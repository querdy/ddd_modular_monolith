from litestar.pagination import OffsetPagination

from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.domain.enities.permission import Permission
from src.user_service.presentation.pagination import PermissionOffsetPagination


class GetPermissionsUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def execute(self, limit: int, offset: int, **filters) -> OffsetPagination[Permission]:
        async with self.uow:
            return await PermissionOffsetPagination(self.uow)(limit, offset, **filters)
