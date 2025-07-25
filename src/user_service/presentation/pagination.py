from src.common.litestar_.pagination import FilteredAbstractAsyncOffsetPaginator
from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.infrastructure.read_models.role import PermissionRead


class PermissionOffsetPagination(FilteredAbstractAsyncOffsetPaginator):
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def get_total(self, **filters) -> int:
        return await self.uow.permissions_read.count(**filters)

    async def get_items(self, limit: int, offset: int, **filters) -> list[PermissionRead]:
        return await self.uow.permissions_read.get_many(limit, offset, **filters)
