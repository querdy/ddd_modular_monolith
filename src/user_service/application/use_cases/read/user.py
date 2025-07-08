from uuid import UUID

from loguru import logger
from sqlalchemy.exc import NoResultFound

from src.user_service.application.exceptions import ApplicationError
from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.infrastructure.read_models.user import UserRead


class GetUserByIdUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def execute(self, user_id: UUID) -> UserRead:
        async with self.uow:
            try:
                user = await self.uow.users_read.get(user_id)
            except NoResultFound:
                raise ApplicationError(f"Пользователь с ID {user_id} не найден")
            return user


class GetUsersUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def execute(self) -> list[UserRead]:
        async with self.uow:
            return await self.uow.users_read.get_all()
