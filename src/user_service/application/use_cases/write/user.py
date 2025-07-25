from uuid import UUID

from loguru import logger

from src.common.exceptions.application import ApplicationPermissionDeniedError
from src.common.message_bus.interfaces import IMessageBus
from src.common.exceptions.application import ApplicationError
from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.application.events import UserCreatedEvent
from src.user_service.application.use_cases.role import GetOrCreateDefaultRoleUseCase
from src.user_service.domain.aggregates.user import User
from src.user_service.domain.enities.user_role_assignment import UserRoleAssignment
from src.common.exceptions.infrastructure import InfrastructureError
from src.user_service.infrastructure.read_models.user import UserRead


class RegisterUserUseCase:
    def __init__(self, uow: IUserServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(self, username: str, email: str, password: str, repeat_password: str) -> User:
        async with self.uow:
            try:
                existing_user = await self.uow.users.get_by_email(email)
                if existing_user:
                    raise ApplicationError(f"Пользователь с email {email} уже существует")
            except InfrastructureError:
                ...
            role = await GetOrCreateDefaultRoleUseCase(self.uow).execute()
            user = User.create(
                username=username,
                email=email,
                password=password,
                repeat_password=repeat_password,
                role_assignment=UserRoleAssignment.create(role_id=role.id),
            )
            await self.uow.users.add(user)
            await self.mb.publish(UserCreatedEvent.model_validate(user))
            return user


class AssignRoleUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def execute(self, user_id: UUID, role_id: UUID, term: int | None) -> UserRead:
        async with self.uow:
            try:
                user = await self.uow.users.get(user_id)
                role = await self.uow.roles.get(role_id)
            except InfrastructureError:
                raise

            user.assign_role(role.id, term)
            user = await self.uow.users.update(user)
            await self.uow.session.flush()
            return await self.uow.users_read.get(user.id)


class UnsignRoleUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def execute(self, user_id: UUID, role_id: UUID) -> UserRead:
        async with self.uow:
            user = await self.uow.users.get(user_id)
            user.remove_role(role_id)
            user = await self.uow.users.update(user)
            await self.uow.session.flush()
            return await self.uow.users_read.get(user.id)


class ChangePasswordUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def execute(
        self, user_id: UUID, current_user_id: UUID, old_password: str, new_password: str, repeat_password: str
    ) -> None:
        logger.info(f"{user_id} {current_user_id} {old_password} {new_password} {repeat_password}")
        async with self.uow:
            if user_id != current_user_id:
                raise ApplicationPermissionDeniedError(
                    f"У вас недостаточно прав для изменения пароля другому пользователю"
                )
            user = await self.uow.users.get(user_id)
            user.change_password(old_password, new_password, repeat_password)
            await self.uow.users.update(user)
