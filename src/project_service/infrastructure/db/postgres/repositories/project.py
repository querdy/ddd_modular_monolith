from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions.infrastructure import InfrastructureError
from src.project_service.domain.aggregates.project import Project
from src.project_service.infrastructure.db.postgres.models import ProjectModel
from src.project_service.infrastructure.mappers.project import project_to_orm, project_to_domain


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, project: Project) -> None:
        orm_project = project_to_orm(project)
        self.session.add(orm_project)

    async def get(self, project_id: UUID) -> Project:
        stmt = select(ProjectModel).where(ProjectModel.id == project_id)
        result = await self.session.execute(stmt)
        try:
            orm_project = result.scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Проект с ID {project_id} не найден")
        return project_to_domain(orm_project)
