from uuid import UUID

from litestar.pagination import OffsetPagination

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.aggregates.project import Project
from src.project_service.presentation.pagination import ProjectOffsetPagination


class GetProjectUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, project_id: UUID) -> Project:
        async with self.uow:
            project = await self.uow.projects.get(project_id)
            return project


class GetProjectsUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, limit: int, offset: int) -> OffsetPagination[Project]:
        async with self.uow:
            return await ProjectOffsetPagination(uow=self.uow)(limit, offset)
            # projects = await self.uow.projects.get_many()
            # return projects
