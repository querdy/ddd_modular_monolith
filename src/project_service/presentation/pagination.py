from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic

from litestar.pagination import OffsetPagination

from src.project_service.application.protocols import IProjectServiceUoW


T = TypeVar("T")


class FilteredAbstractAsyncOffsetPaginator(ABC, Generic[T]):
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


class ProjectOffsetPagination(FilteredAbstractAsyncOffsetPaginator):
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def get_total(self, **filters) -> int:
        return await self.uow.projects.count()

    async def get_items(self, limit: int, offset: int, **filters) -> list[T]:
        return await self.uow.projects.get_many(limit, offset)


class SubprojectOffsetPagination(FilteredAbstractAsyncOffsetPaginator):
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def get_total(self, **filters) -> int:
        return await self.uow.projects_read.subprojects_count(**filters)

    async def get_items(self, limit: int, offset: int, **filters) -> list[T]:
        return await self.uow.projects_read.get_subprojects(limit, offset, **filters)


class StageOffsetPagination(FilteredAbstractAsyncOffsetPaginator):
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def get_total(self, **filters) -> int:
        return await self.uow.projects_read.stages_count(**filters)

    async def get_items(self, limit: int, offset: int, **filters) -> list[T]:
        return await self.uow.projects_read.get_stages(limit, offset, **filters)
