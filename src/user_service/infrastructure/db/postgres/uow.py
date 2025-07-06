from typing import Self

from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.user_service.application.protocols import IUserRepository, IRoleRepository, IUserReadRepository
from src.user_service.config import settings
from src.user_service.infrastructure.db.postgres.repositories.role import RoleRepository
from src.user_service.infrastructure.db.postgres.repositories.user import UserRepository, UserReadRepository


class UoWUserService:
    users: IUserRepository
    users_read: IUserReadRepository
    roles: IRoleRepository

    def __init__(self, database_url: str = settings.DB_STRING):
        engine = create_async_engine(database_url, echo=False, future=True)
        self.sessionmaker = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> Self:
        self.session = self.sessionmaker()
        self.users = UserRepository(self.session)
        self.users_read = UserReadRepository(self.session)
        self.roles = RoleRepository(self.session)
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
