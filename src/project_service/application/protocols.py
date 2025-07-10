from typing import Self, Protocol
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.project_service.domain.aggregates.project import Project


class IProjectRepository(Protocol):
    async def add(self, project: Project) -> None: ...
    async def get(self, project_id: UUID) -> Project: ...


class IProjectServiceUoW(Protocol):
    """Интерфейс для UoW"""

    session: AsyncSession
    projects: IProjectRepository

    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
