from uuid import UUID

from litestar.pagination import OffsetPagination

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.entities.stage import Stage
from src.project_service.presentation.pagination import StageOffsetPagination


class GetStageUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, stage_id: UUID) -> Stage:
        async with self.uow:
            project = await self.uow.projects.get_by_stage(stage_id)
            stage = project.get_stage_by_id(stage_id)
            return stage


class GetStagesUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, limit: int, offset: int, **filters) -> OffsetPagination[Stage]:
        async with self.uow:
            return await StageOffsetPagination(self.uow)(limit, offset, **filters)
