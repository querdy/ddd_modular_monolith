from typing import Callable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from src.user_service.application.protocols import IUserServiceUoW

from src.user_service.config import settings
from src.user_service.infrastructure.db.postgres.uow import UserServiceUoW


class UoWUserServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def get_sessionmaker(self) -> async_sessionmaker:
        engine = create_async_engine(settings.DB_STRING, echo=False, future=True)
        return async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    @provide(scope=Scope.REQUEST)
    def get_uow(self, sessionmaker: async_sessionmaker) -> IUserServiceUoW:
        return UserServiceUoW(sessionmaker())

    @provide(scope=Scope.REQUEST)
    def get_uow_factory(self, sessionmaker: async_sessionmaker) -> Callable[[], IUserServiceUoW]:
        def factory() -> IUserServiceUoW:
            return UserServiceUoW(sessionmaker())

        return factory
