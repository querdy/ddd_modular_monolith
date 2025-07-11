from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions.infrastructure import InfrastructureError
from src.project_service.application.protocols import IProjectReadRepository
from src.project_service.domain.aggregates.project import Project
from src.project_service.domain.entities.stage import Stage
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.infrastructure.db.postgres.models import ProjectModel, SubprojectModel, StageModel
from src.project_service.infrastructure.mappers.project import project_to_orm, project_to_domain
from src.project_service.infrastructure.mappers.stage import stage_to_domain
from src.project_service.infrastructure.mappers.subproject import subproject_to_domain


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def count(self) -> int:
        stmt = select(func.count(ProjectModel.id))
        result = await self.session.execute(stmt)
        return result.scalar()

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

    async def get_many(self, limit: int, offset: int) -> list[Project]:
        stmt = select(ProjectModel).limit(limit).offset(offset)
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

    async def get_subproject_by_id(self, subproject_id: UUID) -> Subproject: ...

    async def subprojects_count(self, **filters) -> int:
        stmt = select(func.count()).select_from(SubprojectModel)
        if project_id := filters.get("project_id", False):
            stmt = stmt.where(SubprojectModel.project_id == project_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_subprojects(self, limit: int, offset: int, **filters) -> list[Subproject]:
        stmt = select(SubprojectModel).limit(limit).offset(offset)
        if project_id := filters.get("project_id", False):
            stmt = stmt.where(SubprojectModel.project_id == project_id)
        result = await self.session.execute(stmt)
        orm_subprojects = result.scalars().all()
        return [subproject_to_domain(subproject) for subproject in orm_subprojects]

    async def stages_count(self, **filters) -> int:
        stmt = select(func.count()).select_from(StageModel)
        if subproject_id := filters.get("subproject_id", False):
            stmt = stmt.where(StageModel.subproject_id == subproject_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_stages(self, limit: int, offset: int, **filters) -> list[Stage]:
        stmt = select(StageModel).limit(limit).offset(offset)
        if subproject_id := filters.get("subproject_id", False):
            stmt = stmt.where(StageModel.subproject_id == subproject_id)
        result = await self.session.execute(stmt)
        orm_stages = result.scalars().all()
        return [stage_to_domain(stage) for stage in orm_stages]
