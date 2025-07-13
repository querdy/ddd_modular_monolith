from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic

from litestar.pagination import OffsetPagination

from src.common.pagination import FilteredAbstractAsyncOffsetPaginator
from src.project_service.application.protocols import IProjectServiceUoW

T = TypeVar("T")


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
