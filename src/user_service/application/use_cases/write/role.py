from uuid import UUID

from loguru import logger

from src.common.exceptions.application import ApplicationError
from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.domain.aggregates.role import Role


class UpdateRoleUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def execute(self, role_id: UUID, name: str, permission_ids: list[UUID]) -> Role:
        async with self.uow:
            permissions = await self.uow.permissions.get_by_ids(permission_ids)
            if len(permissions) != len(permission_ids):
                raise ApplicationError(f"Передан некорректный список разрешений")
            role = await self.uow.roles.get(role_id)
            role.update(
                name=name,
                permissions=permissions,
            )
            await self.uow.roles.update(role)
            return role
