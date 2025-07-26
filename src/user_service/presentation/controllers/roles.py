from uuid import UUID

from dishka import FromDishka
from litestar import Controller, get, post, put
from litestar.dto import DTOData

from src.common.litestar_.guards.permission import PermissionGuard
from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.application.use_cases.role import GetRolesUseCase, GetRoleByIdUseCase, CreateRoleUseCase
from src.user_service.application.use_cases.write.role import UpdateRoleUseCase
from src.user_service.domain.aggregates.role import Role
from src.user_service.infrastructure.read_models.role import RoleRead
from src.user_service.presentation.dto.role import (
    RoleWithPermissionsResponseDTO,
    RoleShortResponseDTO,
    CreateRoleRequestDTO,
    UpdateRoleRequestDTO,
)
from src.user_service.presentation.schemas.role import CreateRoleRequestSchema, UpdateRoleRequestSchema


class RoleController(Controller):
    path = "/roles"
    tags = ["Роли"]

    @get(
        path="",
        return_dto=RoleShortResponseDTO,
        guards=[PermissionGuard("roles:read")],
        summary="Получить список всех ролей",
    )
    async def list(self, uow: FromDishka[IUserServiceUoW]) -> list[Role]:
        use_case = GetRolesUseCase(uow)
        result = await use_case.execute()
        return result

    @get(
        path="/{role_id: uuid}",
        return_dto=RoleWithPermissionsResponseDTO,
        guards=[PermissionGuard("roles:read")],
        summary="Получить роль по ID",
    )
    async def get(self, role_id: UUID, uow: FromDishka[IUserServiceUoW]) -> Role:
        use_case = GetRoleByIdUseCase(uow)
        result = await use_case.execute(role_id)
        return result

    @post(
        path="",
        dto=CreateRoleRequestDTO,
        guards=[PermissionGuard("roles:write")],
        return_dto=RoleWithPermissionsResponseDTO,
        summary="Создать роль",
    )
    async def create(self, data: DTOData[CreateRoleRequestSchema], uow: FromDishka[IUserServiceUoW]) -> Role:
        data_instance = data.create_instance()
        use_case = CreateRoleUseCase(uow)
        result = await use_case.execute(data_instance.name)
        return result

    @put(
        path="/{role_id: uuid}",
        dto=UpdateRoleRequestDTO,
        guards=[PermissionGuard("roles:write")],
        summary="Полное обновление роли",
    )
    async def put(
        self, role_id: UUID, data: DTOData[UpdateRoleRequestSchema], uow: FromDishka[IUserServiceUoW]
    ) -> Role:
        data_instance = data.create_instance()
        use_case = UpdateRoleUseCase(uow)
        result = await use_case.execute(role_id, data_instance.name, data_instance.permission_ids)
        return result
