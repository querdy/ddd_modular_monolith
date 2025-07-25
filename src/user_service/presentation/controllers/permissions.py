from dataclasses import asdict

from dishka import FromDishka
from litestar import Controller, get
from litestar.pagination import OffsetPagination

from src.common.litestar_.di.filters import get_limit_offset_filters, LimitOffsetFilterRequest
from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.application.use_cases.read.permission import GetPermissionsUseCase
from src.user_service.domain.enities.permission import Permission
from src.user_service.presentation.di.filters import get_permissions_filters
from src.user_service.presentation.schemas.permission import (
    FilterPermissionsRequestSchema,
)


class PermissionController(Controller):
    path = "/permissions"
    tags = ["Разрешения"]

    @get(
        path="",
        dependencies={"filters": get_permissions_filters, "pagination": get_limit_offset_filters},
        summary="Получение списка разрешений",
    )
    async def list(
        self,
        pagination: LimitOffsetFilterRequest,
        filters: FilterPermissionsRequestSchema,
        uow: FromDishka[IUserServiceUoW],
    ) -> OffsetPagination[Permission]:
        use_case = GetPermissionsUseCase(uow)
        result = await use_case.execute(limit=pagination.limit, offset=pagination.offset, **asdict(filters))
        return result

    # @post(path="", dto=CreatePermissionRequestDTO, summary="Создание нового разрешения")
    # @inject
    # async def create(
    #     self, data: DTOData[CreatePermissionRequestSchema], uow: FromDishka[IUserServiceUoW]
    # ) -> Permission:
    #     data_instance = data.create_instance()
    #     use_case = CreatePermissionUseCase(uow)
    #     result = await use_case.execute(data_instance.code, data_instance.description)
    #     return result
