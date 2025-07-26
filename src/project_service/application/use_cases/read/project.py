from uuid import UUID

from litestar.pagination import OffsetPagination
from loguru import logger

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.aggregates.project import Project
from src.project_service.infrastructure.read_models.project import ProjectRead
from src.project_service.presentation.pagination import ProjectOffsetPagination


class GetProjectUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, project_id: UUID) -> Project:
        async with self.uow:
            project = await self.uow.projects_read.get_project(project_id)
            return project


class GetProjectsUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, limit: int, offset: int) -> OffsetPagination[Project]:
        async with self.uow:
            return await ProjectOffsetPagination(uow=self.uow)(limit, offset)
