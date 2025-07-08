from uuid import UUID

from loguru import logger
from sqlalchemy.exc import NoResultFound

from src.common.message_bus.interfaces import IMessageBus
from src.user_service.application.exceptions import ApplicationError
from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.application.events import UserCreatedEvent
from src.user_service.application.use_cases.queries import GetInfoQuery, GetInfoResponse
from src.user_service.application.use_cases.role import GetOrCreateDefaultRoleUseCase
from src.user_service.domain.aggregates.user import User
from src.user_service.domain.enities.user_role_assignment import UserRoleAssignment
from src.user_service.infrastructure.exceptions import InfrastructureError
from src.user_service.infrastructure.read_models.user import UserRead


class RegisterUserUseCase:
    def __init__(self, uow: IUserServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(self, username: str, email: str, password: str) -> User:
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
                role_assignment=UserRoleAssignment.create(role_id=role.id),
            )
            await self.uow.users.add(user)
            await self.mb.publish(UserCreatedEvent(id=user.id, username=username, email=email))
            a = await self.mb.query(GetInfoQuery(user_id=str(user.id)), response_model=GetInfoResponse)
            logger.info(a)
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
            # roles = await self.uow.roles.get_many(
            #     [role_assignment.role_id for role_assignment in user.role_assignments]
            # )
            # role_mapper = {role.id: role for role in roles}
            #
            # return UserWithRolesDTO(
            #     id=user.id,
            #     username=user.username,
            #     email=user.email,
            #     role_assignments=[
            #         UserRoleAssignmentWithRolesDTO(
            #             expires_at=role_assignment.expires_at,
            #             role=RoleDTO(
            #                 id=role_mapper[role_assignment.role_id].id,
            #                 name=role_mapper[role_assignment.role_id].name,
            #                 permissions=[
            #                     PermissionDTO(code=permission.code, description=permission.description)
            #                     for permission in role_mapper[role_assignment.role_id].permissions
            #                     if role_assignment.role_id in role_mapper
            #                 ],
            #             ),
            #         )
            #         for role_assignment in user.role_assignments
            #         if role_assignment.role_id in role_mapper
            #     ],
            # )
