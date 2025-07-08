from typing import Annotated, Callable

from dishka import Provider, Scope, provide, FromComponent
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from src.user_service.application.protocols import (
    IUserServiceUoW,
    IUserRepository,
    IRoleRepository,
    IUserReadRepository,
)
from src.user_service.config import settings
from src.user_service.infrastructure.db.postgres.repositories.role import RoleRepository
from src.user_service.infrastructure.db.postgres.repositories.user import UserRepository, UserReadRepository
from src.user_service.infrastructure.db.postgres.uow import UserServiceUoW

#
# class UoWUserServiceProvider(Provider):
#     @provide(scope=Scope.REQUEST)
#     async def provide_uow(self) -> IUserServiceUoW:
#         return UoWUserService()


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

# class RepositoryProvider(Provider):
#     # component = "repository"
#
#     # @provide(scope=Scope.REQUEST)
#     # def get_user_repository(self, session: Annotated[AsyncSession, FromComponent("database")]) -> IUserRepository:
#     #     return UserRepository(session)
#     #
#     # @provide(scope=Scope.REQUEST)
#     # def get_user_read_repository(
#     #     self, session: Annotated[AsyncSession, FromComponent("database")]
#     # ) -> IUserReadRepository:
#     #     return UserReadRepository(session)
#     #
#     # @provide(scope=Scope.REQUEST)
#     # def get_role_repository(self, session: Annotated[AsyncSession, FromComponent("database")]) -> IRoleRepository:
#     #     return RoleRepository(session)
#
#     @provide(scope=Scope.REQUEST)
#     def get_uow(self, session: Annotated[AsyncSession, FromComponent("database")]) -> IUserServiceUoW:
#         return UoWUserService(session)
