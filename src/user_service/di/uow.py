from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.user_service.application.protocols import IUnitOfWork, IUserRepository, IRoleRepository
from src.user_service.config import settings
from src.user_service.infrastructure.db.postgres.repositories.role import RoleRepository
from src.user_service.infrastructure.db.postgres.repositories.user import UserRepository
from src.user_service.infrastructure.db.postgres.uow import UoWPostgres


# class UoWProvider(Provider):
#     @provide(scope=Scope.REQUEST)
#     async def provide_uow(self) -> IUnitOfWork:
#         return UoWPostgres()


class DatabaseProvider(Provider):
    component = "database"

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
    def get_session(self, sessionmaker: async_sessionmaker) -> AsyncSession:
        return sessionmaker()

class RepositoryProvider(Provider):
    component = "repository"

    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> IUserRepository:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_role_repository(self, session: AsyncSession) -> IRoleRepository:
        return RoleRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_uow(
        self,
        session: AsyncSession,
        users: IUserRepository,
        roles: IRoleRepository,
    ) -> UoWPostgres:
        return UoWPostgres(session=session, users=users, roles=roles)