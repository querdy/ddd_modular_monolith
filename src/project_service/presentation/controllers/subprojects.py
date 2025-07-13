from dataclasses import asdict
from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, post, get, delete, patch
from litestar.dto import DTOData
from litestar.pagination import OffsetPagination
from litestar.params import Parameter

from src.common.di.filters import get_limit_offset_filters, LimitOffsetFilterRequest
from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.application.use_cases.read.subproject import GetSubprojectUseCase, GetSubprojectsUseCase
from src.project_service.application.use_cases.write.subproject import (
    CreateSubprojectUseCase,
    DeleteSubprojectUseCase,
    UpdateSubprojectUseCase,
)
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.presentation.di.filters import get_subproject_filters
from src.project_service.presentation.dto.subproject import (
    SubprojectCreateRequestDTO,
    SubprojectCreateResponseDTO,
    SubprojectResponseDTO,
    SubprojectShortResponseDTO,
    SubprojectUpdateRequestDTO,
)
from src.project_service.presentation.pagination import SubprojectOffsetPagination
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
        summary="Создание нового подпроекта",
    )
    @inject
    async def create(
        self,
        data: DTOData[SubprojectCreateRequestSchema],
        uow: FromDishka[IProjectServiceUoW],
    ) -> Subproject:
        data_instance = data.create_instance()
        use_case = CreateSubprojectUseCase(uow)
        result = await use_case.execute(data_instance.project_id, data_instance.name, data_instance.description)
        return result

    @get(
        path="",
        return_dto=SubprojectShortResponseDTO,
        dependencies={"filters": get_subproject_filters, "pagination": get_limit_offset_filters},
        summary="Получение подпроектов",
    )
    @inject
    async def list(
        self,
        pagination: LimitOffsetFilterRequest,
        filters: FilterSubprojectsRequestSchema,
        uow: FromDishka[IProjectServiceUoW],
    ) -> OffsetPagination[Subproject]:
        use_case = GetSubprojectsUseCase(uow)
        result = await use_case.execute(limit=pagination.limit, offset=pagination.offset, **asdict(filters))
        return result

    @get(path="/{subproject_id: uuid}", return_dto=SubprojectShortResponseDTO, summary="Получение подпроекта по ID")
    @inject
    async def get(self, subproject_id: UUID, uow: FromDishka[IProjectServiceUoW]) -> Subproject:
        use_case = GetSubprojectUseCase(uow)
        result = await use_case.execute(subproject_id)
        return result

    @delete(path="/{subproject_id: uuid}", summary="Удаление проекта")
    @inject
    async def delete(self, subproject_id: UUID, uow: FromDishka[IProjectServiceUoW]) -> None:
        use_case = DeleteSubprojectUseCase(uow)
        await use_case.execute(subproject_id)

    @patch(path="/{subproject_id: uuid}", dto=SubprojectUpdateRequestDTO, summary="Обновление подпроекта")
    @inject
    async def update(
        self, subproject_id: UUID, data: DTOData[SubprojectUpdateRequestSchema], uow: FromDishka[IProjectServiceUoW]
    ) -> Subproject:
        data_instance = data.create_instance()
        use_case = UpdateSubprojectUseCase(uow)
        result = await use_case.execute(subproject_id, data_instance.name, data_instance.description)
        return result
