from dishka import FromDishka

from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.domain.aggregates.permission import Permission


class CreatePermissionUseCase:
    def __init__(self, uow: FromDishka[IUserServiceUoW]):
        self.uow = uow

    async def execute(self, code: str, description: str) -> Permission:
        async with self.uow:
            new_permission = Permission.create(code, description)
            await self.uow.permissions.add(new_permission)
            return new_permission
