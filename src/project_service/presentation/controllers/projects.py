from uuid import UUID

from dishka import FromDishka
from litestar import Controller, post, get, delete, put
from litestar.dto import DTOData

from src.common.litestar_.di.filters import get_limit_offset_filters, LimitOffsetFilterRequest
from src.common.litestar_.guards.permission import PermissionGuard
from src.common.message_bus.interfaces import IMessageBus
from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.application.use_cases.read.project import GetProjectUseCase, GetProjectsUseCase
from src.project_service.application.use_cases.write.project import (
    CreateProjectUseCase,
    DeleteProjectUseCase,
    UpdateProjectUseCase,
    CreateTemplateForProjectUseCase,
)
from src.project_service.domain.aggregates.project import Project
from src.project_service.presentation.dto.project import (
    ProjectCreateRequestDTO,
    ProjectCreateResponseDTO,
    ProjectShortResponseDTO,
    ProjectResponseDTO,
    ProjectUpdateRequestDTO,
    CreateTemplateRequestDTO,
)
from src.project_service.presentation.schemas.project import (
    ProjectCreateSchema,
    ProjectUpdateRequestSchema,
    CreateTemplateRequestSchema,
)
from litestar.pagination import OffsetPagination


class ProjectsController(Controller):
    path = "/projects"
    tags = ["Проекты"]

    @post(
        path="",
        dto=ProjectCreateRequestDTO,
        return_dto=ProjectCreateResponseDTO,
        guards=[PermissionGuard("projects:write")],
        summary="Создание нового проекта",
    )
    async def create(
        self,
        data: DTOData[ProjectCreateSchema],
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> Project:
        data_instance = data.create_instance()
        use_case = CreateProjectUseCase(uow, mb)
        result = await use_case.execute(data_instance.name, data_instance.description)
        return result

    @get(
        path="",
        return_dto=ProjectShortResponseDTO,
        dependencies={"pagination": get_limit_offset_filters},
        guards=[PermissionGuard("projects:read")],
        summary="Получить проекты",
    )
    async def list(
        self,
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
        pagination: LimitOffsetFilterRequest,
    ) -> OffsetPagination[Project]:
        use_case = GetProjectsUseCase(uow)
        result = await use_case.execute(limit=pagination.limit, offset=pagination.offset)
        return result

    @get(
        path="/{project_id: uuid}",
        return_dto=ProjectResponseDTO,
        guards=[PermissionGuard("projects:read")],
        summary="Получение проекта по ID",
    )
    async def get(self, project_id: UUID, uow: FromDishka[IProjectServiceUoW]) -> Project:
        use_case = GetProjectUseCase(uow)
        result = await use_case.execute(project_id)
        return result

    @post(
        path="/{project_id: uuid}/template",
        dto=CreateTemplateRequestDTO,
        return_dto=ProjectResponseDTO,
        guards=[PermissionGuard("projects:write")],
        summary="Создание шаблона на основе подпроекта",
    )
    async def make_template(
        self,
        project_id: UUID,
        data: DTOData[CreateTemplateRequestSchema],
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> Project:
        data_instance = data.create_instance()
        use_case = CreateTemplateForProjectUseCase(uow, mb)
        result = await use_case.execute(project_id, data_instance.subproject_id)
        return result

    @delete(
        path="/{project_id: uuid}",
        guards=[PermissionGuard("projects:write")],
        summary="Удаление проекта",
    )
    async def delete(
        self,
        project_id: UUID,
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> None:
        use_case = DeleteProjectUseCase(uow, mb)
        await use_case.execute(project_id)

    @put(
        path="/{project_id: uuid}",
        dto=ProjectUpdateRequestDTO,
        return_dto=ProjectShortResponseDTO,
        guards=[PermissionGuard("projects:write")],
        summary="Обновление проекта",
    )
    async def update(
        self,
        project_id: UUID,
        data: DTOData[ProjectUpdateRequestSchema],
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> Project:
        data_instance = data.create_instance()
        use_case = UpdateProjectUseCase(uow, mb)
        result = await use_case.execute(project_id, data_instance.name, data_instance.description)
        return result
