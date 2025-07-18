from dataclasses import asdict
from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, post, get, patch, delete, Request, put
from litestar.dto import DTOData
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from loguru import logger

from src.common.di.filters import get_limit_offset_filters, LimitOffsetFilterRequest
from src.common.message_bus.interfaces import IMessageBus
from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.application.use_cases.read.stage import GetStageUseCase, GetStagesUseCase
from src.project_service.application.use_cases.write.stage import (
    CreateStageUseCase,
    UpdateStageUseCase,
    DeleteStageUseCase,
    ChangeStageStatusUseCase,
)
from src.project_service.domain.entities.stage import Stage
from src.project_service.domain.value_objects.enums import StageStatus
from src.project_service.infrastructure.read_models.stage import StageRead
from src.project_service.presentation.di.filters import get_stage_filters
from src.project_service.presentation.dto.stage import (
    StageCreateRequestDTO,
    StageCreateResponseDTO,
    StageResponseDTO,
    StageShortResponseDTO,
    StageUpdateRequestDTO,
    ChangeStageStatusRequestDTO, StageReadResponseDTO,
)
from src.project_service.presentation.schemas.stage import (
    StageCreateRequestSchema,
    FilterStageRequestSchema,
    StageUpdateRequestSchema,
    ChangeStageStatusRequestSchema,
)


class StagesController(Controller):
    path = "/stages"
    tags = ["Этапы"]

    @post(
        path="", dto=StageCreateRequestDTO, return_dto=StageCreateResponseDTO, summary="Добавление этапа к подпроекту"
    )
    @inject
    async def create(self, data: DTOData[StageCreateRequestSchema], uow: FromDishka[IProjectServiceUoW]) -> Stage:
        data_instance = data.create_instance()
        use_case = CreateStageUseCase(uow)
        result = await use_case.execute(data_instance.subproject_id, data_instance.name, data_instance.description)
        return result

    @get(
        path="",
        return_dto=StageResponseDTO,
        dependencies={"filters": get_stage_filters, "pagination": get_limit_offset_filters},
        summary="Получение этапов",
    )
    @inject
    async def list(
        self,
        pagination: LimitOffsetFilterRequest,
        filters: FilterStageRequestSchema,
        uow: FromDishka[IProjectServiceUoW],
    ) -> OffsetPagination[Stage]:
        use_case = GetStagesUseCase(uow)
        result = await use_case.execute(limit=pagination.limit, offset=pagination.offset, **asdict(filters))
        return result

    @get(path="/{stage_id: uuid}", return_dto=StageResponseDTO, summary="Получение этапа по ID")
    @inject
    async def get(self, stage_id: UUID, uow: FromDishka[IProjectServiceUoW]) -> Stage:
        use_case = GetStageUseCase(uow)
        result = await use_case.execute(stage_id)
        return result

    @put(
        path="/{stage_id: uuid}",
        dto=StageUpdateRequestDTO,
        return_dto=StageShortResponseDTO,
        summary="Изменение этапа",
        description=f"Статусы: {', '.join(f'"{s.value}"' for s in StageStatus)}",
    )
    @inject
    async def update(
        self, stage_id: UUID, data: DTOData[StageUpdateRequestSchema], uow: FromDishka[IProjectServiceUoW]
    ) -> Stage:
        data_instance = data.create_instance()
        use_case = UpdateStageUseCase(uow)
        result = await use_case.execute(stage_id, data_instance.name, data_instance.description)
        return result

    @delete(path="/{stage_id: uuid}", summary="Удаление этапа")
    @inject
    async def delete(self, stage_id: UUID, uow: FromDishka[IProjectServiceUoW]) -> None:
        use_case = DeleteStageUseCase(uow)
        await use_case.execute(stage_id)

    @patch(path="/{stage_id: uuid}/change_status", dto=ChangeStageStatusRequestDTO, return_dto=StageReadResponseDTO, summary="Обновление статуса этапа")
    @inject
    async def change_status(
        self,
        request: Request,
        stage_id: UUID,
        data: DTOData[ChangeStageStatusRequestSchema],
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> StageRead:
        data_instance = data.create_instance()
        use_case = ChangeStageStatusUseCase(uow, mb)
        result = await use_case.execute(stage_id, data_instance.status, UUID(request.auth.sub), data_instance.message)
        return result
