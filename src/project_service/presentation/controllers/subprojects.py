from dataclasses import asdict
from uuid import UUID

from dishka import FromDishka
from litestar import Controller, post, get, delete, put
from litestar.dto import DTOData
from litestar.pagination import OffsetPagination

from src.common.litestar_.di.filters import get_limit_offset_filters, LimitOffsetFilterRequest
from src.common.litestar_.guards.permission import PermissionGuard
from src.common.message_bus.interfaces import IMessageBus
from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.application.use_cases.read.subproject import GetSubprojectUseCase, GetSubprojectsUseCase
from src.project_service.application.use_cases.write.subproject import (
    CreateSubprojectUseCase,
    DeleteSubprojectUseCase,
    UpdateSubprojectUseCase,
)
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.infrastructure.read_models.subproject import SubprojectRead
from src.project_service.presentation.di.filters import get_subproject_filters
from src.project_service.presentation.dto.subproject import (
    SubprojectCreateRequestDTO,
    SubprojectCreateResponseDTO,
    SubprojectShortResponseDTO,
    SubprojectUpdateRequestDTO, SubprojectReadDTO,
)
from src.project_service.presentation.schemas.subproject import (
    SubprojectCreateRequestSchema,
    FilterSubprojectsRequestSchema,
    SubprojectUpdateRequestSchema,
)


class SubProjectsController(Controller):
    path = "/subprojects"
    tags = ["Подпроекты"]

    @post(
        path="",
        dto=SubprojectCreateRequestDTO,
        return_dto=SubprojectCreateResponseDTO,
        guards=[PermissionGuard("subprojects:write")],
        summary="Создание нового подпроекта",
    )
    async def create(
        self,
        data: DTOData[SubprojectCreateRequestSchema],
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> Subproject:
        data_instance = data.create_instance()
        use_case = CreateSubprojectUseCase(uow, mb)
        result = await use_case.execute(
            data_instance.project_id, data_instance.name, data_instance.description, data_instance.from_template
        )
        return result

    @get(
        path="",
        return_dto=SubprojectReadDTO,
        dependencies={"filters": get_subproject_filters, "pagination": get_limit_offset_filters},
        guards=[PermissionGuard("subprojects:read")],
        summary="Получение подпроектов",
    )
    async def list(
        self,
        pagination: LimitOffsetFilterRequest,
        filters: FilterSubprojectsRequestSchema,
        uow: FromDishka[IProjectServiceUoW],
    ) -> OffsetPagination[SubprojectRead]:
        use_case = GetSubprojectsUseCase(uow)
        result = await use_case.execute(limit=pagination.limit, offset=pagination.offset, **asdict(filters))
        return result

    @get(
        path="/{subproject_id: uuid}",
        return_dto=SubprojectReadDTO,
        guards=[PermissionGuard("subprojects:read")],
        summary="Получение подпроекта по ID",
    )
    async def get(self, subproject_id: UUID, uow: FromDishka[IProjectServiceUoW]) -> SubprojectRead:
        use_case = GetSubprojectUseCase(uow)
        result = await use_case.execute(subproject_id)
        return result

    @delete(
        path="/{subproject_id: uuid}",
        guards=[PermissionGuard("subprojects:write")],
        summary="Удаление проекта",
    )
    async def delete(
        self,
        subproject_id: UUID,
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> None:
        use_case = DeleteSubprojectUseCase(uow, mb)
        await use_case.execute(subproject_id)

    @put(
        path="/{subproject_id: uuid}",
        dto=SubprojectUpdateRequestDTO,
        guards=[PermissionGuard("subprojects:write")],
        summary="Обновление подпроекта",
    )
    async def update(
        self,
        subproject_id: UUID,
        data: DTOData[SubprojectUpdateRequestSchema],
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> Subproject:
        data_instance = data.create_instance()
        use_case = UpdateSubprojectUseCase(uow, mb)
        result = await use_case.execute(subproject_id, data_instance.name, data_instance.description)
        return result
