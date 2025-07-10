from uuid import UUID

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.entities.subproject import Subproject


class GetSubprojectUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, subproject_id: UUID) -> Subproject:
        async with self.uow:
            project = await self.uow.projects.get_by_subproject(subproject_id)
            subproject = project.get_subproject_by_id(subproject_id)
            return subproject
