from uuid import UUID

from sqlalchemy import select, func, delete, desc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload, selectinload, joinedload

from src.common.db.counter import count_queries
from src.common.exceptions.domain import DomainError
from src.common.exceptions.infrastructure import InfrastructureError
from src.project_service.domain.aggregates.project import Project
from src.project_service.domain.entities.stage import Stage
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.infrastructure.db.postgres.models import (
    ProjectModel,
    SubprojectModel,
    StageModel,
    SubprojectTemplateModel,
)
from src.project_service.infrastructure.mappers.project import project_to_orm, project_to_domain
from src.project_service.infrastructure.mappers.stage import stage_to_domain
from src.project_service.infrastructure.mappers.subproject import subproject_to_domain
from src.project_service.infrastructure.read_models.subproject import SubprojectRead


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @count_queries
    async def count(self) -> int:
        stmt = select(func.count(ProjectModel.id))
        result = await self.session.execute(stmt)
        return result.scalar()

    @count_queries
    async def add(self, project: Project) -> None:
        orm_project = project_to_orm(project)
        self.session.add(orm_project)

    @count_queries
    async def get(self, project_id: UUID) -> Project:
        stmt = (
            select(ProjectModel)
            .where(ProjectModel.id == project_id)
            .options(
                joinedload(ProjectModel.template).joinedload(SubprojectTemplateModel.stages),
                selectinload(ProjectModel.files),
                selectinload(ProjectModel.subprojects)
                .selectinload(SubprojectModel.stages)
                .selectinload(StageModel.messages),
            )
        )
        result = await self.session.execute(stmt)
        try:
            orm_project = result.unique().scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Проект с ID {project_id} не найден")
        return project_to_domain(orm_project)

    @count_queries
    async def get_many(self, limit: int, offset: int) -> list[Project]:
        stmt = (
            select(ProjectModel)
            .limit(limit)
            .offset(offset)
            .order_by(desc(ProjectModel.created_at))
            .options(
                selectinload(ProjectModel.files),
                selectinload(ProjectModel.subprojects)
                .selectinload(SubprojectModel.stages)
                .selectinload(StageModel.messages),
            )
        )
        result = await self.session.execute(stmt)
        orm_projects = result.scalars().all()
        return [project_to_domain(orm_project) for orm_project in orm_projects]

    @count_queries
    async def update(self, project: Project) -> Project:
        orm_project = project_to_orm(project)
        new_project = await self.session.merge(
            orm_project,
            options=[
                joinedload(ProjectModel.template).selectinload(SubprojectTemplateModel.stages),
                selectinload(ProjectModel.files),
                selectinload(ProjectModel.subprojects)
                .selectinload(SubprojectModel.stages)
                .selectinload(StageModel.messages),
            ],
        )
        return project_to_domain(new_project)

    @count_queries
    async def get_by_subproject(self, subproject_id: UUID) -> Project:
        stmt = (
            select(SubprojectModel)
            .where(SubprojectModel.id == subproject_id)
            .options(joinedload(SubprojectModel.project))
        )
        result_subproject = await self.session.execute(stmt)
        subproject = result_subproject.scalar_one_or_none()

        if subproject is None or subproject.project is None:
            raise InfrastructureError(f"Проект, содержащий подпроект с ID {subproject_id}, не найден")

        stmt_project = (
            select(ProjectModel)
            .where(ProjectModel.id == subproject.project.id)
            .options(
                joinedload(ProjectModel.template).selectinload(SubprojectTemplateModel.stages),
                selectinload(ProjectModel.files),
                selectinload(ProjectModel.subprojects)
                .selectinload(SubprojectModel.files),
                selectinload(ProjectModel.subprojects)
                .selectinload(SubprojectModel.stages)
                .selectinload(StageModel.messages),
                selectinload(ProjectModel.subprojects)
                .selectinload(SubprojectModel.stages)
                .selectinload(StageModel.files),
            )
        )
        result_project = await self.session.execute(stmt_project)
        orm_project = result_project.unique().scalar_one_or_none()

        if orm_project is None:
            raise InfrastructureError(f"Проект, содержащий подпроект с ID {subproject_id}, не найден")
        return project_to_domain(orm_project)

    @count_queries
    async def get_by_stage(self, stage_id: UUID) -> Project:
        stmt = (
            select(StageModel)
            .where(StageModel.id == stage_id)
            .options(joinedload(StageModel.subproject).joinedload(SubprojectModel.project))
        )

        result_stage = await self.session.execute(stmt)
        stage = result_stage.scalar_one_or_none()

        if stage is None or stage.subproject is None or stage.subproject.project is None:
            raise InfrastructureError(f"Проект, содержащий этап с ID {stage_id}, не найден")

        stmt = (
            select(ProjectModel)
            .where(ProjectModel.id == stage.subproject.project.id)
            .options(
                joinedload(ProjectModel.template).joinedload(SubprojectTemplateModel.stages),
                selectinload(ProjectModel.files),
                selectinload(ProjectModel.subprojects)
                .selectinload(SubprojectModel.files),
                selectinload(ProjectModel.subprojects)
                .selectinload(SubprojectModel.stages)
                .selectinload(StageModel.files),
                selectinload(ProjectModel.subprojects)
                .selectinload(SubprojectModel.stages)
                .selectinload(StageModel.messages),
            )
        )
        result = await self.session.execute(stmt)
        orm_project = result.unique().scalar_one_or_none()
        if orm_project is None:
            raise InfrastructureError(f"Проект, содержащий этап с ID {stage_id}, не найден")
        return project_to_domain(orm_project)

    async def delete(self, project_id: UUID) -> None:
        stmt = delete(ProjectModel).where(ProjectModel.id == project_id)
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise DomainError("Проект с указанным ID отсутствует")


class ProjectReadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @count_queries
    async def subprojects_count(self, **filters) -> int:
        stmt = select(func.count()).select_from(SubprojectModel)
        if project_id := filters.get("project_id", False):
            stmt = stmt.where(SubprojectModel.project_id == project_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    @count_queries
    async def get_subprojects(self, limit: int, offset: int, **filters) -> list[SubprojectRead]:
        stmt = (
            select(SubprojectModel)
            .limit(limit)
            .offset(offset)
            .order_by(desc(SubprojectModel.updated_at))
            .options(
                noload(SubprojectModel.stages),
                noload(SubprojectModel.project),
                noload(SubprojectModel.files),
            )
        )
        if project_id := filters.get("project_id", False):
            stmt = stmt.where(SubprojectModel.project_id == project_id)
        result = await self.session.execute(stmt)
        orm_subprojects = result.scalars().all()
        return [SubprojectRead.model_validate(orm_subproject) for orm_subproject in orm_subprojects]

    @count_queries
    async def get_subproject(self, subproject_id: UUID) -> SubprojectRead:
        stmt = (
            select(SubprojectModel)
            .where(SubprojectModel.id == subproject_id)
            .options(
                selectinload(SubprojectModel.files),
                noload(SubprojectModel.stages),
                noload(SubprojectModel.project),
            )
        )
        result = await self.session.execute(stmt)
        try:
            orm_subproject = result.scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Подпроект с ID {subproject_id} не найден")
        return SubprojectRead.model_validate(orm_subproject)

    @count_queries
    async def stages_count(self, **filters) -> int:
        stmt = select(func.count()).select_from(StageModel)
        if subproject_id := filters.get("subproject_id", False):
            stmt = stmt.where(StageModel.subproject_id == subproject_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    @count_queries
    async def get_stages(self, limit: int, offset: int, **filters) -> list[Stage]:
        stmt = (
            select(StageModel)
            .order_by(desc(StageModel.updated_at))
            .limit(limit)
            .offset(offset)
            .options(
                noload(StageModel.files),
                selectinload(StageModel.messages),
            )
        )
        if subproject_id := filters.get("subproject_id", False):
            stmt = stmt.where(StageModel.subproject_id == subproject_id)
        result = await self.session.execute(stmt)
        orm_stages = result.unique().scalars().all()
        return [stage_to_domain(stage) for stage in orm_stages]

    @count_queries
    async def get_stage(self, stage_id: UUID) -> Stage:
        stmt = (
            select(StageModel)
            .where(StageModel.id == stage_id)
            .options(
                selectinload(StageModel.files),
                selectinload(StageModel.messages),
            )
        )
        result = await self.session.execute(stmt)
        try:
            orm_stage = result.scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Этап с ID {stage_id}, не найден")
        return stage_to_domain(orm_stage)

    @count_queries
    async def get_projects(self, limit: int, offset: int, **filters) -> list[Project]:
        stmt = (
            select(ProjectModel)
            .limit(limit)
            .offset(offset)
            .order_by(desc(ProjectModel.created_at))
            .options(
                noload(ProjectModel.template),
                noload(ProjectModel.subprojects),
                noload(ProjectModel.files),
            )
        )
        result = await self.session.execute(stmt)
        orm_projects = result.scalars().all()
        # return [ProjectRead.model_validate(orm_project) for orm_project in orm_projects]
        return [project_to_domain(orm_project) for orm_project in orm_projects]

    @count_queries
    async def get_project(self, project_id: UUID) -> Project:
        stmt = (
            select(ProjectModel)
            .where(ProjectModel.id == project_id)
            .order_by(desc(ProjectModel.created_at))
            .options(
                joinedload(ProjectModel.template)
                .joinedload(SubprojectTemplateModel.stages),
                selectinload(ProjectModel.files),
                noload(ProjectModel.subprojects),
            )
        )
        result = await self.session.execute(stmt)
        try:
            orm_project = result.unique().scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Проект с ID {project_id} не найден")
        return project_to_domain(orm_project)
