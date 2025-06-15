from typing import Protocol, Self

from sqlalchemy.ext.asyncio import AsyncSession


class IUserRepository(Protocol):
    """Интерфейс для репозитория пользователей."""
    ...

class IRoleRepository(Protocol):
    """Интерфейс для репозитория ролей."""
    ...

class IUnitOfWork(Protocol):
    """Интерфейс для UoW"""
    session: AsyncSession
    users: IUserRepository
    roles: IRoleRepository

    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...