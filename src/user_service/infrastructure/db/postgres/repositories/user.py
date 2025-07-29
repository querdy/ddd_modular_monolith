from uuid import UUID

from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload, selectinload, joinedload

from src.common.db.counter import count_queries
from src.user_service.domain.aggregates.user import User
from src.common.exceptions.infrastructure import InfrastructureError
from src.user_service.infrastructure.read_models.user import UserRead
from src.user_service.infrastructure.db.postgres.models import UserModel, UserRoleAssignmentModel, RoleModel
from src.user_service.infrastructure.mappers.user import user_to_domain, user_to_orm


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @count_queries
    async def get(self, user_id: UUID) -> User:
        stmt = (
            select(UserModel)
            .where(UserModel.id == user_id)
            .options(
                joinedload(UserModel.role_assignments)
                .joinedload(UserRoleAssignmentModel.role)
                .selectinload(RoleModel.permissions)
            )
        )
        result = await self.session.execute(stmt)
        try:
            orm_user = result.unique().scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Пользователь с ID {user_id} не найден")
        return user_to_domain(orm_user)

    @count_queries
    async def get_by_email(self, email: str) -> User:
        stmt = (
            select(UserModel)
            .where(UserModel.email == email)
            .options(
                selectinload(UserModel.role_assignments)
                .joinedload(UserRoleAssignmentModel.role)
                .selectinload(RoleModel.permissions)
            )
        )
        result = await self.session.execute(stmt)
        try:
            orm_user = result.scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Пользователь с email {email} не найден")
        return user_to_domain(orm_user)

    @count_queries
    async def get_all(self) -> list[User]:
        stmt = select(UserModel).options(noload(UserModel.role_assignments))
        result = await self.session.execute(stmt)
        orm_users = result.scalars().all()
        return [user_to_domain(orm_user) for orm_user in orm_users]

    @count_queries
    async def add(self, user: User) -> None:
        orm_user = user_to_orm(user)
        self.session.add(orm_user)

    @count_queries
    async def update(self, user: User) -> User:
        orm_user = user_to_orm(user)
        new_user = await self.session.merge(orm_user)
        return user_to_domain(new_user)


class UserReadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @count_queries
    async def get(self, user_id: UUID) -> UserRead:
        stmt = (
            select(UserModel)
            .where(UserModel.id == user_id)
            .options(
                selectinload(UserModel.role_assignments)
                .joinedload(UserRoleAssignmentModel.role)
                .selectinload(RoleModel.permissions)
            )
        )
        result = await self.session.execute(stmt)
        try:
            orm_user = result.scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Пользователь с ID {user_id} не найден")
        return UserRead.model_validate(orm_user)

    @count_queries
    async def get_many(self, user_ids: list[UUID] = None) -> list[UserRead]:
        stmt = select(UserModel).options(noload(UserModel.role_assignments))
        if user_ids is not None:
            stmt = stmt.where(UserModel.id.in_(user_ids))
        result = await self.session.execute(stmt)
        orm_users = result.scalars().all()
        return [UserRead.model_validate(orm_user) for orm_user in orm_users]

    @count_queries
    async def get_by_email(self, email: str) -> UserRead:
        stmt = (
            select(UserModel)
            .where(UserModel.email == email)
            .options(
                selectinload(UserModel.role_assignments)
                .joinedload(UserRoleAssignmentModel.role)
                .selectinload(RoleModel.permissions)
            )
        )
        result = await self.session.execute(stmt)
        try:
            orm_user = result.scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Пользователь с email {email} не найден")
        return UserRead.model_validate(orm_user)
