from uuid import UUID

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.aggregates.project import Project


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

    async def execute(self) -> list[Project]:
        async with self.uow:
            projects = await self.uow.projects.get_all()
            return projects
