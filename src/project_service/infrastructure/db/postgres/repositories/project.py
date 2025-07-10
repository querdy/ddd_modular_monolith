from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions.infrastructure import InfrastructureError
from src.project_service.domain.aggregates.project import Project
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.infrastructure.db.postgres.models import ProjectModel, SubprojectModel, StageModel
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

    async def get_all(self) -> list[Project]:
        stmt = select(ProjectModel)
        result = await self.session.execute(stmt)
        orm_users = result.scalars().all()
        return [project_to_domain(orm_user) for orm_user in orm_users]

    async def update(self, project: Project) -> Project:
        orm_project = project_to_orm(project)
        new_project = await self.session.merge(orm_project)
        return project_to_domain(new_project)

    async def get_by_subproject(self, subproject_id: UUID) -> Project:
        stmt = select(ProjectModel).join(SubprojectModel).where(SubprojectModel.id == subproject_id)
        result = await self.session.execute(stmt)
        try:
            orm_project = result.scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Проект, содержащий подпроект с ID {subproject_id} не найден")
        return project_to_domain(orm_project)

    async def get_by_stage(self, stage_id: UUID) -> Project:
        stmt = (
            select(ProjectModel)
            .join(SubprojectModel, SubprojectModel.project_id == ProjectModel.id)
            .join(StageModel, StageModel.subproject_id == SubprojectModel.id)
            .where(StageModel.id == stage_id)
        )
        result = await self.session.execute(stmt)
        try:
            orm_project = result.scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Проект, содержащий этап с ID {stage_id}, не найден")

        return project_to_domain(orm_project)


class ProjectReadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def get_subproject_by_id(self, subproject_id: UUID) -> Subproject: ...
