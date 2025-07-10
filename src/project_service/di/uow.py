from typing import Callable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.infrastructure.db.postgres.uow import ProjectServiceUoW
from src.user_service.config import settings


class UoWProjectServiceProvider(Provider):
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
    def get_uow(self, sessionmaker: async_sessionmaker) -> IProjectServiceUoW:
        return ProjectServiceUoW(sessionmaker())

    @provide(scope=Scope.REQUEST)
    def get_uow_factory(self, sessionmaker: async_sessionmaker) -> Callable[[], IProjectServiceUoW]:
        def factory() -> IProjectServiceUoW:
            return ProjectServiceUoW(sessionmaker())

        return factory
