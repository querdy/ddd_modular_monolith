from dishka import Provider, Scope, provide

from src.user_service.application.protocols import (
    IUserServiceUoW,
)
from src.user_service.infrastructure.db.postgres.uow import UoWUserService


class UoWUserServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_uow(self) -> IUserServiceUoW:
        return UoWUserService()


# class DatabaseProvider(Provider):
#     component = "database"
#
#     @provide(scope=Scope.APP)
#     def get_sessionmaker(self) -> async_sessionmaker:
#         engine = create_async_engine(settings.DB_STRING, echo=False, future=True)
#         return async_sessionmaker(
#             autocommit=False,
#             autoflush=False,
#             bind=engine,
#             expire_on_commit=False,
#             class_=AsyncSession,
#         )
#
#     @provide(scope=Scope.REQUEST)
#     def get_session(self, sessionmaker: async_sessionmaker) -> AsyncSession:
#         return sessionmaker()
#
# class RepositoryProvider(Provider):
#     component = "repository"
#
#     @provide(scope=Scope.REQUEST)
#     def get_user_repository(self, session: AsyncSession) -> IUserRepository:
#         return UserRepository(session)
#
#     @provide(scope=Scope.REQUEST)
#     def get_role_repository(self, session: AsyncSession) -> IRoleRepository:
#         return RoleRepository(session)
#
#     @provide(scope=Scope.REQUEST)
#     def get_uow(
#         self,
#         session: AsyncSession,
#         users: IUserRepository,
#         roles: IRoleRepository,
#     ) -> UoWPostgres:
#         return UoWPostgres(session=session, users=users, roles=roles)
