from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload

from src.common.exceptions.infrastructure import InfrastructureError
from src.user_service.domain.enities.permission import Permission
from src.user_service.infrastructure.db.postgres.models import PermissionModel, RoleModel
from src.user_service.infrastructure.mappers.role import permission_to_orm, permission_to_domain
from src.user_service.infrastructure.read_models.permission import PermissionRead


class PermissionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, permission: Permission):
        orm_model = permission_to_orm(permission)
        self.session.add(orm_model)

    async def get(self, permission_id: UUID) -> Permission:
        stmt = select(PermissionModel).where(PermissionModel.id == permission_id)
        result = await self.session.execute(stmt)
        orm_permission = result.scalar()
        return permission_to_domain(orm_permission)

    async def get_by_ids(self, permission_ids: list[UUID]) -> list[Permission]:
        stmt = (
            select(PermissionModel).where(PermissionModel.id.in_(permission_ids)).options(noload(PermissionModel.roles))
        )
        result = await self.session.execute(stmt)
        orm_permissions = result.scalars().all()
        return [permission_to_domain(permission) for permission in orm_permissions]

    async def get_by_code(self, code: str) -> Permission:
        stmt = select(PermissionModel).where(PermissionModel.code == code)
        result = await self.session.execute(stmt)
        try:
            orm_permission = result.scalar_one()
        except NoResultFound:
            raise InfrastructureError(f"Пользователь с code {code} не найден")
        return permission_to_domain(orm_permission)


class PermissionReadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def count(self, **filters) -> int:
        stmt = select(func.count()).select_from(PermissionModel)
        if role_id := filters.get("role_id", None):
            stmt = stmt.join(PermissionModel.roles).where(RoleModel.id == role_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_many(self, limit: int, offset: int, **filters) -> list[PermissionRead]:
        stmt = select(PermissionModel).limit(limit).offset(offset).options(noload(PermissionModel.roles))
        if role_id := filters.get("role_id", False):
            stmt = stmt.join(PermissionModel.roles).where(RoleModel.id == role_id)
        result = await self.session.execute(stmt)
        orm_permissions = result.scalars().all()
        return [PermissionRead.model_validate(permission) for permission in orm_permissions]
