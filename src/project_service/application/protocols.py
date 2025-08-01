from typing import Self, Protocol
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.project_service.domain.aggregates.project import Project
from src.project_service.domain.entities.stage import Stage
from src.project_service.domain.entities.stage_status_history import StageStatusHistory
from src.project_service.domain.entities.subproject import Subproject


class IProjectRepository(Protocol):
    async def count(self) -> int: ...
    async def add(self, project: Project) -> None: ...
    async def get(self, project_id: UUID) -> Project: ...
    async def get_many(self, limit: int, offset: int) -> list[Project]: ...
    async def update(self, project: Project) -> Project: ...
    async def get_by_subproject(self, subproject_id: UUID) -> Project: ...
    async def get_by_stage(self, stage_id: UUID) -> Project: ...
    async def delete(self, project_id: UUID) -> None: ...


class IProjectReadRepository(Protocol):
    async def subprojects_count(self, **filters) -> int: ...
    async def get_subprojects(self, limit: int, offset: int, **filters) -> list[Subproject]: ...
    async def get_subproject(self, subproject_id: UUID) -> Subproject: ...
    async def stages_count(self, **filters) -> int: ...
    async def get_stages(self, limit: int, offset: int, **filters) -> list[Stage]: ...
    async def get_stage(self, stage_id: UUID) -> Stage: ...
    async def get_projects(self, limit: int, offset: int, **filters) -> list[Project]: ...
    async def get_project(self, project_id: UUID) -> Project: ...


class IStageStatusHistoryRepository(Protocol):
    async def add(self, obj: StageStatusHistory) -> None: ...
    async def count(self, **filters) -> int: ...
    async def get_many(self, limit: int, offset: int, **filters) -> list[StageStatusHistory]: ...


class IProjectServiceUoW(Protocol):
    """Интерфейс для UoW"""

    session: AsyncSession
    projects: IProjectRepository
    projects_read: IProjectReadRepository
    stage_status_history: IStageStatusHistoryRepository

    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
