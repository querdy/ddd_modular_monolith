from uuid import UUID

from litestar.pagination import OffsetPagination

from src.common.message_bus.interfaces import IMessageBus
from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.entities.stage import Stage
from src.project_service.infrastructure.read_models.stage import StageRead
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
    def __init__(self, uow: IProjectServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(self, limit: int, offset: int, **filters) -> OffsetPagination[StageRead]:
        async with self.uow:
            return await StageOffsetPagination(self.uow, self.mb)(limit, offset, **filters)
