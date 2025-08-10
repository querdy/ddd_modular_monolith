from uuid import UUID

from litestar.pagination import OffsetPagination

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.infrastructure.read_models.subproject import SubprojectRead
from src.project_service.presentation.pagination import SubprojectOffsetPagination


class GetSubprojectUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, subproject_id: UUID) -> SubprojectRead:
        async with self.uow:
            subproject = await self.uow.projects_read.get_subproject(subproject_id)
            return subproject


class GetSubprojectsUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, limit: int, offset: int, **filters) -> OffsetPagination[SubprojectRead]:
        async with self.uow:
            subprojects = await self.uow.projects_read.get_subprojects(limit=limit, offset=offset, **filters)
            total = await self.uow.projects_read.subprojects_count(**filters)
            return SubprojectOffsetPagination.create(subprojects, total, limit, offset)
