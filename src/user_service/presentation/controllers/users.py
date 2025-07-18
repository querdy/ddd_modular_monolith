import asyncio
from typing import Callable
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import get, Controller, Request, post
from litestar.dto import DTOData

from src.common.message_bus.interfaces import IMessageBus
from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.application.use_cases.write.user import (
    RegisterUserUseCase,
    AssignRoleUseCase,
    UnsignRoleUseCase,
)
from src.user_service.application.use_cases.read.user import (
    GetUsersUseCase,
    GetUserByIdUseCase,
)
from src.user_service.domain.aggregates.user import User
from src.user_service.infrastructure.read_models.user import UserRead
from src.user_service.presentation.dto.role import AssignRoleRequestDTO, UnsignRoleRequestDTO
from src.user_service.presentation.schemas.role import AssignRoleRequestSchema, UnsignRoleRequestSchema

from src.user_service.presentation.schemas.user import CreateUserRequestSchema
from src.user_service.presentation.dto.user import (
    UserCreateRequestDto,
    UserCreateResponseDto,
    UserShortResponseDTO,
    UserReadResponseDTO,
)
from src.common.guards.permission import PermissionGuard


class UserController(Controller):
    path = "/users"
    tags = ["Пользователи"]

    @get(
        path="",
        return_dto=UserShortResponseDTO,
        guards=[PermissionGuard("user_read")],
        summary="Получить список всех пользователей",
    )
    @inject
    async def get_all(self, uow: FromDishka[IUserServiceUoW]) -> list[UserRead]:
        use_case = GetUsersUseCase(uow)
        result = await use_case.execute()
        return result

    @get(
        path="/me",
        return_dto=UserReadResponseDTO,
        guards=[PermissionGuard("user_read")],
        summary="Получить текущего (авторизованного) пользователя",
    )
    @inject
    async def get_me(self, request: Request, uow: FromDishka[IUserServiceUoW]) -> UserRead:
        use_case = GetUserByIdUseCase(uow)
        result = await use_case.execute(request.auth.sub)
        return result

    @get(
        path="/{user_id: uuid}",
        return_dto=UserReadResponseDTO,
        guards=[PermissionGuard("user_read")],
        summary="Получить пользователя по ID",
    )
    @inject
    async def get_by_id(self, user_id: UUID, uow: FromDishka[IUserServiceUoW]) -> UserRead:
        use_case = GetUserByIdUseCase(uow)
        result = await use_case.execute(user_id)
        return result

    @post(
        path="",
        dto=UserCreateRequestDto,
        return_dto=UserCreateResponseDto,
        exclude_from_auth=True,
        # guards=[PermissionGuard("user_write")],
        summary="Создать нового пользователя",
    )
    @inject
    async def create(
        self, uow: FromDishka[IUserServiceUoW], mb: FromDishka[IMessageBus], data: DTOData[CreateUserRequestSchema]
    ) -> User:
        data_instance = data.create_instance()
        use_case = RegisterUserUseCase(uow, mb)
        result = await use_case.execute(
            data_instance.username,
            data_instance.email,
            data_instance.password,
            data_instance.repeat_password,
        )
        return result

    @post(
        path="/{user_id: uuid}/assign_role",
        dto=AssignRoleRequestDTO,
        return_dto=UserReadResponseDTO,
        guards=[PermissionGuard("role_write")],
        summary="Назначить роль пользователю",
    )
    @inject
    async def assign_role(
        self, user_id: UUID, data: DTOData[AssignRoleRequestSchema], uow: FromDishka[IUserServiceUoW]
    ) -> UserRead:
        data_instance = data.create_instance()
        use_case = AssignRoleUseCase(uow)
        result = await use_case.execute(user_id, data_instance.role_id, data_instance.term)
        return result

    @post(
        path="/{user_id: uuid}/unassign_role",
        dto=UnsignRoleRequestDTO,
        return_dto=UserReadResponseDTO,
        guards=[PermissionGuard("role_write")],
        summary="Удалить роль у пользователя",
    )
    @inject
    async def unassign_role(
        self, user_id: UUID, data: DTOData[UnsignRoleRequestSchema], uow: FromDishka[IUserServiceUoW]
    ) -> UserRead:
        data_instance = data.create_instance()
        use_case = UnsignRoleUseCase(uow)
        result = await use_case.execute(user_id, data_instance.role_id)
        return result
