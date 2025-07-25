from typing import TypeVar
from uuid import UUID

from src.common.message_bus.interfaces import IMessageBus
from src.common.message_bus.schemas import GetUserInfoListQuery, GetUserInfoListResponse, GetUserInfoResponse
from src.common.litestar_.pagination import FilteredAbstractAsyncOffsetPaginator
from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.infrastructure.read_models.message import MessageRead
from src.project_service.infrastructure.read_models.stage import StageRead

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
    def __init__(self, uow: IProjectServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def get_total(self, **filters) -> int:
        return await self.uow.projects_read.stages_count(**filters)

    async def get_items(self, limit: int, offset: int, **filters) -> list[T]:
        stages = await self.uow.projects_read.get_stages(limit, offset, **filters)

        author_ids = {msg.author_id for stage in stages for msg in stage.messages}
        user_map: dict[UUID, GetUserInfoResponse] = {}
        query_result = await self.mb.query(
            GetUserInfoListQuery(ids=list(author_ids)), response_model=GetUserInfoListResponse
        )
        for user in query_result.users:
            user_map[user.id] = user
        return [
            StageRead(
                id=stage.id,
                name=stage.name,
                description=stage.description,
                created_at=stage.created_at,
                updated_at=stage.updated_at,
                status=stage.status,
                messages=[
                    MessageRead(
                        id=msg.id, created_at=msg.created_at, text=msg.text, author=user_map.get(msg.author_id, None).model_dump()
                    )
                    for msg in stage.messages
                ],
            )
            for stage in stages
        ]
