from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from src.project_service.application.protocols import IProjectRepository, IProjectReadRepository
from src.project_service.infrastructure.db.postgres.repositories.project import ProjectRepository, ProjectReadRepository


class ProjectServiceUoW:
    session: AsyncSession
    projects: IProjectRepository
    projects_read: IProjectReadRepository

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> Self:
        self.projects = ProjectRepository(self.session)
        self.projects_read = ProjectReadRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
