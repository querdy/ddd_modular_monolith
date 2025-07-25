from uuid import UUID

from loguru import logger
from sqlalchemy import select, func, delete, desc, asc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, noload, selectinload, joinedload

from src.common.exceptions.domain import DomainError
from src.common.exceptions.infrastructure import InfrastructureError
from src.project_service.application.protocols import IProjectReadRepository
from src.project_service.domain.aggregates.project import Project
from src.project_service.domain.entities.stage import Stage
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.infrastructure.db.postgres.models import (
    ProjectModel,
    SubprojectModel,
    StageModel,
    MessageModel,
)
from src.project_service.infrastructure.mappers.project import project_to_orm, project_to_domain
from src.project_service.infrastructure.mappers.stage import stage_to_domain
from src.project_service.infrastructure.mappers.subproject import subproject_to_domain
from src.project_service.infrastructure.read_models.project import ProjectRead
from src.project_service.infrastructure.read_models.stage import StageRead
from src.project_service.infrastructure.read_models.subproject import SubprojectRead


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
        stmt = (
            select(ProjectModel)
            .where(ProjectModel.id == project_id)
            .options(
                joinedload(ProjectModel.template),
                selectinload(ProjectModel.subprojects)
                .selectinload(SubprojectModel.stages)
                .selectinload(StageModel.messages)
            )
        )
        result = await self.session.execute(stmt)
        try:
            orm_project = result.scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Проект с ID {project_id} не найден")
        return project_to_domain(orm_project)

    async def get_many(self, limit: int, offset: int) -> list[Project]:
        stmt = select(ProjectModel).limit(limit).offset(offset).order_by(desc(ProjectModel.created_at)).options(
            selectinload(ProjectModel.subprojects)
            .selectinload(SubprojectModel.stages)
            .selectinload(StageModel.messages)
        )
        result = await self.session.execute(stmt)
        orm_projects = result.scalars().all()
        return [project_to_domain(orm_project) for orm_project in orm_projects]

    async def update(self, project: Project) -> Project:
        orm_project = project_to_orm(project)
        new_project = await self.session.merge(orm_project)
        return project_to_domain(new_project)

    async def get_by_subproject(self, subproject_id: UUID) -> Project:
        stmt = (select(ProjectModel)
        .join(SubprojectModel, SubprojectModel.project_id == ProjectModel.id)
        .where(SubprojectModel.id == subproject_id)
        .options(
            joinedload(ProjectModel.template),
            selectinload(ProjectModel.subprojects)
            .selectinload(SubprojectModel.stages)
            .selectinload(StageModel.messages)
        ))
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
            .options(
                joinedload(ProjectModel.template),
                selectinload(ProjectModel.subprojects)
                .selectinload(SubprojectModel.stages)
                .selectinload(StageModel.messages)
            )
        )
        result = await self.session.execute(stmt)
        try:
            orm_project = result.unique().scalar_one()
        except NoResultFound:
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

    async def get_subproject_by_id(self, subproject_id: UUID) -> Subproject:
        ...

    async def subprojects_count(self, **filters) -> int:
        stmt = select(func.count()).select_from(SubprojectModel)
        if project_id := filters.get("project_id", False):
            stmt = stmt.where(SubprojectModel.project_id == project_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_subprojects(self, limit: int, offset: int, **filters) -> list[SubprojectRead]:
        stmt = (
            select(SubprojectModel)
            .limit(limit)
            .offset(offset)
            .order_by(desc(SubprojectModel.updated_at))
            .options(
                noload(SubprojectModel.stages),
            #     selectinload(SubprojectModel.stages)
            #     .selectinload(StageModel.messages)
            )
        )
        if project_id := filters.get("project_id", False):
            stmt = stmt.where(SubprojectModel.project_id == project_id)
        result = await self.session.execute(stmt)
        orm_subprojects = result.scalars().all()
        return [SubprojectRead.model_validate(subproject) for subproject in orm_subprojects]

    async def stages_count(self, **filters) -> int:
        stmt = select(func.count()).select_from(StageModel)
        if subproject_id := filters.get("subproject_id", False):
            stmt = stmt.where(StageModel.subproject_id == subproject_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_stages(self, limit: int, offset: int, **filters) -> list[Stage]:
        stmt = (
            select(StageModel)
            .order_by(desc(StageModel.updated_at))
            .limit(limit)
            .offset(offset)
            .options(
                selectinload(StageModel.messages)
            )
        )
        if subproject_id := filters.get("subproject_id", False):
            stmt = stmt.where(StageModel.subproject_id == subproject_id)
        result = await self.session.execute(stmt)
        orm_stages = result.unique().scalars().all()
        return [stage_to_domain(stage) for stage in orm_stages]

    async def get_stage(self, stage_id: UUID) -> Stage:
        stmt = (
            select(StageModel)
            .where(StageModel.id == stage_id)
            .options(
                selectinload(StageModel.messages)
            )
        )
        result = await self.session.execute(stmt)
        try:
            orm_stage = result.scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Этап с ID {stage_id}, не найден")
        return stage_to_domain(orm_stage)

    async def get_projects(self, limit: int, offset: int, **filters) -> list[ProjectRead]:
        stmt = (
            select(ProjectModel)
            .limit(limit)
            .offset(offset)
            .order_by(desc(ProjectModel.created_at))
            .options(
                joinedload(ProjectModel.template),
                noload(ProjectModel.subprojects)
            )
            # .join(SubprojectModel, SubprojectModel.project_id == ProjectModel.id)
            # .join(StageModel, StageModel.subproject_id == SubprojectModel.id)
            # .join(MessageModel, MessageModel.stage_id == StageModel.id)
            # .options(
            #     joinedload(ProjectModel.template),
            #     selectinload(ProjectModel.subprojects)
            #     .selectinload(SubprojectModel.stages)
            #     .selectinload(StageModel.messages)
            # )
        )
        result = await self.session.execute(stmt)
        orm_projects = result.scalars().all()
        return [ProjectRead.model_validate(orm_project) for orm_project in orm_projects]

    async def get_project(self, project_id: UUID) -> ProjectRead:
        stmt = (
            select(ProjectModel)
            .where(ProjectModel.id == project_id)
            .order_by(desc(ProjectModel.created_at))
            .options(
                # selectinload(ProjectModel.subprojects),
                joinedload(ProjectModel.template),
                noload(ProjectModel.subprojects)
                # selectinload(ProjectModel.subprojects).noload(SubprojectModel.stages)
            )
        )
        result = await self.session.execute(stmt)
        try:
            orm_project = result.scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Проект с ID {project_id} не найден")
        return ProjectRead.model_validate(orm_project)