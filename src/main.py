from dishka.integrations.litestar import setup_dishka as ls_setup_dishka, LitestarProvider, DishkaRouter
from dishka.integrations.faststream import setup_dishka as fs_setup_dishka
from dishka import make_async_container, Scope
from faststream import FastStream

from litestar import Litestar, Router
from litestar.config.cors import CORSConfig
from litestar.middleware import DefineMiddleware
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import (
    SwaggerRenderPlugin,
    RedocRenderPlugin,
    RapidocRenderPlugin,
    StoplightRenderPlugin,
    ScalarRenderPlugin,
)
from litestar.openapi.spec import Components, SecurityScheme
from loguru import logger

from src.common.litestar_.di.message_bus import MessagingProvider
from src.common.exceptions.application import ApplicationError
from src.common.exceptions.infrastructure import InfrastructureError
from src.common.litestar_.exception_handlers import log_exception
from src.common.litestar_.monitoring.prometheus import CustomPrometheusController, prometheus_config
from src.common.message_bus.broker import broker
from src.common.loggers.config import litestar_config
from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.di.uow import UoWProjectServiceProvider
from src.project_service.domain.aggregates.project import Project
from src.project_service.domain.entities.stage import Stage
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.presentation.controllers.projects import ProjectsController
from src.project_service.presentation.controllers.stages import StagesController
from src.project_service.presentation.controllers.subprojects import SubProjectsController
from src.user_service.application import IUserServiceUoW
from src.user_service.application.use_cases.write.permission import GetOrCreateDefaultPermissionsUseCase
from src.user_service.di.uow import UoWUserServiceProvider
from src.user_service.domain.aggregates.role import Role
from src.user_service.domain.aggregates.user import User
from src.user_service.domain.default_objects.permissions import default_permissions
from src.common.exceptions.domain import DomainError
from src.user_service.domain.enities.user_role_assignment import UserRoleAssignment
from src.user_service.presentation.controllers.auth import AuthController
from src.user_service.presentation.controllers.permissions import PermissionController
from src.user_service.presentation.controllers.roles import RoleController
from src.user_service.presentation.controllers.users import UserController
from src.user_service.presentation.middlewares.auth import AuthMiddleware

container = make_async_container(
    LitestarProvider(),
    UoWUserServiceProvider(),
    UoWProjectServiceProvider(),
    MessagingProvider(),
)

metric_router = Router(
    path="",
    route_handlers=[
        CustomPrometheusController,
    ],
)

router = DishkaRouter(
    path="/api",
    route_handlers=[
        AuthController,
        UserController,
        RoleController,
        PermissionController,
        ProjectsController,
        SubProjectsController,
        StagesController,
    ],
)

default_role_name = "Администратор"

async def update_admin_role_permissions():
    async with container(scope=Scope.REQUEST) as cont:
        uow = await cont.get(IUserServiceUoW)
        async with uow:
            role = await uow.roles.get_by_name(default_role_name)
            if role is None:
                role = Role.create(default_role_name)
            permissions = await GetOrCreateDefaultPermissionsUseCase(uow).execute(default_permissions)
            for permission in permissions:
                role.add_permission(permission)
            await uow.roles.update(role)

async def create_test_data():
    async with container(scope=Scope.REQUEST) as cont:
        uow = await cont.get(IUserServiceUoW)
        async with uow:
            role = await uow.roles.get_by_name(default_role_name)
            us = await uow.users.get_all()
            if not us:
                await uow.users.add(User.create(username="kekw", email="kekw@gmail.com", password="string123", repeat_password="string123", role_assignment=UserRoleAssignment.create(role_id=role.id)))
        uow = await cont.get(IProjectServiceUoW)
        async with uow:
            pr = await uow.projects_read.get_projects(limit=1, offset=0)
            if not pr:
                for idx in range(20):
                    project = Project.create(name=f"Проект-{idx}")
                    for jdx in range(50):
                        subproject = Subproject.create(name=f"Подпроект-{jdx}")
                        project.add_subproject(subproject)
                        for kdx in range(20):
                            stage = Stage.create(name=f"stage-{kdx}")
                            subproject.add_stage(stage)
                    await uow.projects.add(project)

app = Litestar(
    debug=True,
    route_handlers=[router, metric_router],
    logging_config=litestar_config,
    middleware=[DefineMiddleware(AuthMiddleware), prometheus_config.middleware],
    on_startup=[broker.start, update_admin_role_permissions, create_test_data],
    on_shutdown=[broker.close],
    cors_config=CORSConfig(
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3001"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    ),
    exception_handlers={
        DomainError: log_exception,
        ApplicationError: log_exception,
        InfrastructureError: log_exception,
    },
    openapi_config=OpenAPIConfig(
        title="IT-M Task Tracker",
        version="0.0.1",
        components=Components(
            security_schemes={
                "bearer": SecurityScheme(
                    type="http",
                    scheme="bearer",
                    bearer_format="JWT",
                    description="Access token в формате Bearer <token>",
                ),
            }
        ),
        security=[
            {"bearer": []},
        ],
        path="/docs",
        render_plugins=[
            SwaggerRenderPlugin(path="/swagger"),
            RedocRenderPlugin(path="/redoc"),
            StoplightRenderPlugin(path="/stoplight"),
            RapidocRenderPlugin(path="/rapid"),
            ScalarRenderPlugin(path="/scalar"),
        ],
    ),
)

ls_setup_dishka(container, app)

fs_setup_dishka(container, FastStream(broker))
