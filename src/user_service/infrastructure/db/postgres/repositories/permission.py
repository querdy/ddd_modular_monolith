from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.user_service.domain.aggregates.permission import Permission
from src.user_service.infrastructure.db.postgres.models import PermissionModel, RoleModel
from src.user_service.infrastructure.mappers.role import permission_to_orm, permission_to_domain
from src.user_service.infrastructure.read_models.permission import PermissionRead
from src.user_service.infrastructure.read_models.role import RoleRead


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
        stmt = select(PermissionModel).limit(limit).offset(offset)
        if role_id := filters.get("role_id", False):
            stmt = stmt.join(PermissionModel.roles).where(RoleModel.id == role_id)
        result = await self.session.execute(stmt)
        orm_permissions = result.scalars().all()
        return [PermissionRead.model_validate(permission) for permission in orm_permissions]
