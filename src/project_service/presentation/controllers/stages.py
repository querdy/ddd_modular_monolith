from dataclasses import asdict
from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, post, get
from litestar.dto import DTOData
from litestar.pagination import OffsetPagination
from litestar.params import Parameter

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.application.use_cases.read.stage import GetStageUseCase, GetStagesUseCase
from src.project_service.application.use_cases.write.stage import CreateStageUseCase
from src.project_service.domain.entities.stage import Stage
from src.project_service.presentation.di.filters import get_stage_filters
from src.project_service.presentation.dto.stage import (
    StageCreateRequestDTO,
    StageCreateResponseDTO,
    StageResponseDTO,
    StageShortResponseDTO,
)
from src.project_service.presentation.schemas.stage import StageCreateRequestSchema, FilterStageRequestSchema


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
        return_dto=StageShortResponseDTO,
        dependencies={"filters": get_stage_filters},
        summary="Получение этапов",
    )
    @inject
    async def list(
        self,
        limit: Annotated[int, Parameter(ge=1, le=100, default=100)],
        offset: Annotated[int, Parameter(ge=0, default=0)],
        filters: FilterStageRequestSchema,
        uow: FromDishka[IProjectServiceUoW],
    ) -> OffsetPagination[Stage]:
        use_case = GetStagesUseCase(uow)
        result = await use_case.execute(limit, offset, **asdict(filters))
        return result

    @get(path="/{stage_id: uuid}", return_dto=StageResponseDTO, summary="Получение этапа по ID")
    @inject
    async def get(self, stage_id: UUID, uow: FromDishka[IProjectServiceUoW]) -> Stage:
        use_case = GetStageUseCase(uow)
        result = await use_case.execute(stage_id)
        return result
