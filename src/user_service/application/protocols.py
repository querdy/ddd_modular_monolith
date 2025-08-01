from typing import Protocol, Self
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.user_service.domain.aggregates.blacklist import BlacklistedToken
from src.user_service.domain.enities.permission import Permission
from src.user_service.domain.aggregates.role import Role
from src.user_service.domain.aggregates.user import User
from src.user_service.infrastructure.read_models.permission import PermissionRead
from src.user_service.infrastructure.read_models.role import RoleRead
from src.user_service.infrastructure.read_models.user import UserRead


class IUserRepository(Protocol):
    """Интерфейс для репозитория пользователей."""

    async def get(self, user_id: UUID) -> User: ...
    async def get_by_email(self, email: str) -> User: ...
    async def get_all(self) -> list[User]: ...
    async def add(self, user: User) -> None: ...
    async def update(self, user: User) -> User: ...


class IUserReadRepository(Protocol):
    """Интерфейс для репозитория чтения пользователей."""

    async def get(self, user_id: UUID) -> UserRead: ...
    async def get_by_email(self, email: str) -> UserRead: ...
    async def get_many(self, user_ids: list[UUID] = None) -> list[UserRead]: ...


class IRoleRepository(Protocol):
    """Интерфейс для репозитория ролей."""

    async def get(self, role_id: UUID) -> Role: ...
    async def get_many(self, role_ids: list[UUID]) -> list[Role]: ...
    async def get_by_name(self, name: str) -> Role: ...
    async def add(self, role: Role) -> None: ...
    async def update(self, role: Role) -> Role: ...


class IRoleReadRepository(Protocol):
    """Интерфейс для репозитория чтения ролей."""

    async def get(self, role_id: UUID) -> RoleRead: ...


class IPermissionRepository(Protocol):
    async def add(self, permission: Permission) -> None: ...
    async def get(self, permission_id: UUID) -> Permission: ...
    async def get_by_ids(self, permission_ids: list[UUID]) -> list[Permission]: ...
    async def get_by_code(self, code: str) -> Permission: ...


class IPermissionReadRepository(Protocol):
    async def count(self, **filters) -> int: ...
    async def get_many(self, limit: int, offset: int, **filters) -> list[PermissionRead]: ...


class IBlacklistRepository(Protocol):
    async def add(self, blacklisted_token: BlacklistedToken) -> None: ...
    async def exists(self, blacklisted_token: str) -> bool: ...


class IUserServiceUoW(Protocol):
    """Интерфейс для UoW"""

    session: AsyncSession
    users: IUserRepository
    users_read: IUserReadRepository
    roles: IRoleRepository
    roles_read: IRoleReadRepository
    permissions: IPermissionRepository
    permissions_read: IPermissionReadRepository
    blacklist: IBlacklistRepository

    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
