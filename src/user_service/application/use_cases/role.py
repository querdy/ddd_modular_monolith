from uuid import UUID

from litestar.dto import DTOData
from loguru import logger

from src.common.exceptions.application import ApplicationError
from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.application.use_cases.write.permission import GetOrCreateDefaultPermissionsUseCase
from src.user_service.domain.aggregates.role import Role
from src.user_service.domain.default_objects.permissions import default_permissions
from src.user_service.infrastructure.read_models.role import RoleRead


class GetOrCreateDefaultRoleUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow
        self.default_role_name = "Администратор"

    async def execute(self) -> Role:
        async with self.uow:
            role = await self.uow.roles.get_by_name(self.default_role_name)
            if role is None:
                permissions = await GetOrCreateDefaultPermissionsUseCase(self.uow).execute(default_permissions)
            else:
                return role
        async with self.uow:
            role = Role.create(name=self.default_role_name)
            for permission in permissions:
                role.add_permission(permission)
            await self.uow.roles.update(role)
            return role


class GetRolesByIdsUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def execute(self, role_ids: list[UUID]) -> list[Role]:
        async with self.uow:
            roles = await self.uow.roles.get_many(role_ids)
            return roles


class GetRolesUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def execute(self) -> list[Role]:
        async with self.uow:
            roles = await self.uow.roles.get_many()
            return roles


class GetRoleByIdUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def execute(self, role_id: UUID) -> Role:
        async with self.uow:
            role = await self.uow.roles.get(role_id)
            return role


class CreateRoleUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def execute(self, role_name: str) -> Role:
        async with self.uow:
            exiting_role = await self.uow.roles.get_by_name(role_name)
            if exiting_role:
                raise ApplicationError(f"Роль с именем {role_name} уже существует")
            role = Role.create(name=role_name)
            await self.uow.roles.add(role)
            return role
