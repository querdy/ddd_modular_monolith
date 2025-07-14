from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.user_service.domain.aggregates.role import Role
from src.user_service.infrastructure.db.postgres.models import RoleModel, PermissionModel
from src.user_service.infrastructure.mappers.role import role_to_domain, role_to_orm
from src.user_service.infrastructure.read_models.role import PermissionRead, RoleRead


class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, role_id: UUID) -> Role:
        stmt = select(RoleModel).where(RoleModel.id == role_id)
        result = await self.session.execute(stmt)
        orm_role = result.scalar()
        return role_to_domain(orm_role)

    async def get_many(self, role_ids: list[UUID]) -> list[Role]:
        stmt = select(RoleModel).where(RoleModel.id.in_(role_ids))
        result = await self.session.execute(stmt)
        orm_roles = result.scalars().all()
        return [role_to_domain(orm_role) for orm_role in orm_roles]

    async def get_by_name(self, name: str) -> Role:
        stmt = select(RoleModel).where(RoleModel.name == name)
        result = await self.session.execute(stmt)
        orm_user = result.scalar()
        return role_to_domain(orm_user) if orm_user else None

    async def get_all(self) -> list[Role]:
        stmt = select(RoleModel)
        result = await self.session.execute(stmt)
        orm_roles = result.scalars().all()
        return [role_to_domain(role) for role in orm_roles]

    async def add(self, role: Role) -> None:
        orm_model = role_to_orm(role)
        self.session.add(orm_model)


class RoleReadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, role_id: UUID) -> RoleRead:
        stmt = select(RoleModel).where(RoleModel.id == role_id)
        result = await self.session.execute(stmt)
        orm_role = result.scalar()
        return RoleRead.model_validate(orm_role)
