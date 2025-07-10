from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.aggregates.project import Project


class CreateProjectUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, name: str, description: str) -> Project:
        async with self.uow:
            project = Project.create(name=name, description=description)
            await self.uow.projects.add(project)
            return project
