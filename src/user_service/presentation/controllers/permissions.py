from dataclasses import asdict
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get
from litestar.pagination import OffsetPagination

from src.common.di.filters import get_limit_offset_filters, LimitOffsetFilterRequest
from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.application.use_cases.read.permission import GetPermissionsUseCase
from src.user_service.domain.enities.permission import Permission
from src.user_service.presentation.di.filters import get_permissions_filters
from src.user_service.presentation.schemas.permission import FilterPermissionsRequestSchema


class PermissionController(Controller):
    path = "/permissions"
    tags = ["Разрешения"]

    @get(
        path="",
        dependencies={"filters": get_permissions_filters, "pagination": get_limit_offset_filters},
        summary="Получение списка разрешений",
    )
    @inject
    async def list(
        self,
        pagination: LimitOffsetFilterRequest,
        filters: FilterPermissionsRequestSchema,
        uow: FromDishka[IUserServiceUoW],
    ) -> OffsetPagination[Permission]:
        use_case = GetPermissionsUseCase(uow)
        result = await use_case.execute(**asdict(pagination), **asdict(filters))
        return result
