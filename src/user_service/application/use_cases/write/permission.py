from dishka import FromDishka

from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.domain.aggregates.permission import Permission


class CreatePermissionUseCase:
    def __init__(self, uow: FromDishka[IUserServiceUoW]):
        self.uow = uow

    async def execute(self) -> Permission:
        ...