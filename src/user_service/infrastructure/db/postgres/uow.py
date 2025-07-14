from typing import Self

from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.user_service.application.protocols import (
    IUserRepository,
    IRoleRepository,
    IUserReadRepository,
    IBlacklistRepository,
    IRoleReadRepository,
    IPermissionRepository,
    IPermissionReadRepository,
)
from src.user_service.config import settings
from src.user_service.infrastructure.db.postgres.repositories.blacklist import BlacklistRepository
from src.user_service.infrastructure.db.postgres.repositories.permission import (
    PermissionRepository,
    PermissionReadRepository,
)
from src.user_service.infrastructure.db.postgres.repositories.role import RoleRepository, RoleReadRepository
from src.user_service.infrastructure.db.postgres.repositories.user import UserRepository, UserReadRepository


class UserServiceUoW:
    users: IUserRepository
    users_read: IUserReadRepository
    roles: IRoleRepository
    roles_read: IRoleReadRepository
    permissions: IPermissionRepository
    permissions_read: IPermissionReadRepository
    blacklist: IBlacklistRepository

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> Self:
        self.users = UserRepository(self.session)
        self.users_read = UserReadRepository(self.session)
        self.roles = RoleRepository(self.session)
        self.roles_read = RoleReadRepository(self.session)
        self.permissions = PermissionRepository(self.session)
        self.permissions_read = PermissionReadRepository(self.session)
        self.blacklist = BlacklistRepository(self.session)
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
