from dishka.integrations.litestar import setup_dishka, LitestarProvider
from dishka import make_async_container

from litestar import Litestar, get
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

from src.common.di import MessagingProvider
from src.common.message_bus.broker import broker
from src.project_service.di.uow import UoWProjectServiceProvider
from src.project_service.presentation.controllers.projects import ProjectsController
from src.project_service.presentation.controllers.stages import StagesController
from src.project_service.presentation.controllers.subprojects import SubProjectsController
from src.user_service.di.uow import UoWUserServiceProvider
from src.user_service.presentation.controllers.auth import AuthController
from src.user_service.presentation.controllers.roles import RoleController
from src.user_service.presentation.controllers.users import UserController
from src.user_service.presentation.middlewares.auth import AuthMiddleware

app = Litestar(
    debug=True,
    route_handlers=[
        AuthController,
        UserController,
        RoleController,
        ProjectsController,
        SubProjectsController,
        StagesController,
    ],
    # on_app_init=[jwt_refresh_auth.on_app_init, jwt_access_auth.on_app_init],
    middleware=[DefineMiddleware(AuthMiddleware)],
    on_startup=[broker.start],
    on_shutdown=[broker.close],
    openapi_config=OpenAPIConfig(
        title="Litestar Example",
        description="Example of litestar",
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
        security=[{"bearer": []}],
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

container = make_async_container(
    LitestarProvider(),
    UoWUserServiceProvider(),
    UoWProjectServiceProvider(),
    MessagingProvider(),
)

setup_dishka(container, app)
