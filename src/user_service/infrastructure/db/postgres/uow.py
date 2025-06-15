from typing import Self

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.user_service.application.protocols import IUserRepository, IRoleRepository

class UoWPostgres:
    session: AsyncSession
    users: IUserRepository
    roles: IRoleRepository

    def __init__(
        self,
        session: AsyncSession,
        users: IUserRepository,
        roles: IRoleRepository,
    ):
        self.users = users
        self.roles = roles
        self.session = session

    async def __aenter__(self) -> Self:
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