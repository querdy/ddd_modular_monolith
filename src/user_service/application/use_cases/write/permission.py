from dishka import FromDishka

from src.common.exceptions.infrastructure import InfrastructureError
from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.domain.enities.permission import Permission


class CreatePermissionUseCase:
    def __init__(self, uow: FromDishka[IUserServiceUoW]):
        self.uow = uow

    async def execute(self, code: str, description: str) -> Permission:
        async with self.uow:
            new_permission = Permission.create(code, description)
            await self.uow.permissions.add(new_permission)
            return new_permission


class GetOrCreateDefaultPermissionsUseCase:
    def __init__(self, uow: FromDishka[IUserServiceUoW]):
        self.uow = uow

    async def execute(self, permissions: list[Permission]) -> list[Permission]:
        async with self.uow:
            permission_for_return = []
            for permission in permissions:
                try:
                    new_permission = await self.uow.permissions.get_by_code(permission.code)
                    permission_for_return.append(new_permission)
                except InfrastructureError:
                    await self.uow.permissions.add(permission)
                    permission_for_return.append(permission)
            return permission_for_return
