from uuid import UUID

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.entities.subproject import Subproject


class CreateSubprojectUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, project_id: UUID, name: str, description: str) -> Subproject:
        async with self.uow:
            project = await self.uow.projects.get(project_id)

            subproject = Subproject.create(name=name, description=description)
            project.add_subproject(subproject)
            await self.uow.projects.update(project)
            return subproject


class DeleteSubprojectUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, subproject_id: UUID) -> None:
        async with self.uow:
            project = await self.uow.projects.get_by_subproject(subproject_id)
            project.remove_subproject(subproject_id)
            await self.uow.projects.update(project)


class UpdateSubprojectUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, subproject_id: UUID, name: str | None, description: str | None) -> Subproject:
        async with self.uow:
            project = await self.uow.projects.get_by_subproject(subproject_id)
            subproject = project.update_subproject(subproject_id, name, description)
            await self.uow.projects.update(project)
            return subproject
