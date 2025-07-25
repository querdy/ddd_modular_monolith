from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from litestar.pagination import OffsetPagination, AbstractAsyncOffsetPaginator

T = TypeVar("T")


class FilteredAbstractAsyncOffsetPaginator(AbstractAsyncOffsetPaginator[T]):
    @abstractmethod
    async def get_total(self, **filters) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_items(self, limit: int, offset: int, **filters) -> list[T]:
        raise NotImplementedError

    async def __call__(self, limit: int, offset: int, **filters) -> OffsetPagination[T]:
        total = await self.get_total(**filters)
        items = await self.get_items(limit=limit, offset=offset, **filters)
        return OffsetPagination(items=items, total=total, offset=offset, limit=limit)
