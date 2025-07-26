from uuid import UUID

from litestar.pagination import OffsetPagination

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.presentation.pagination import SubprojectOffsetPagination


class GetSubprojectUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, subproject_id: UUID) -> Subproject:
        async with self.uow:
            subproject = await self.uow.projects_read.get_subproject(subproject_id)
            return subproject


class GetSubprojectsUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, limit: int, offset: int, **filters) -> OffsetPagination[Subproject]:
        async with self.uow:
            return await SubprojectOffsetPagination(self.uow)(limit, offset, **filters)
