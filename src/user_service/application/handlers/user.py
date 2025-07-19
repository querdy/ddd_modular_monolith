from uuid import UUID

from aiocache import cached, SimpleMemoryCache
from dishka import FromDishka
from dishka.integrations.faststream import inject
from loguru import logger

from src.common.message_bus.broker import broker
from src.common.message_bus.schemas import (
    GetUserInfoQuery,
    GetUserInfoResponse,
    GetUserInfoListQuery,
    GetUserInfoListResponse,
)
from src.user_service.application.events import UserCreatedEvent
from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.application.use_cases.queries import GetInfoQuery, GetInfoResponse


@broker.subscriber("usercreatedevent")
async def on_user_created(event: UserCreatedEvent):
    logger.info(event)


@broker.subscriber("getuserinfoquery")
@inject
@cached(ttl=60, cache=SimpleMemoryCache)
async def on_get_user_info(event: GetUserInfoQuery, uow: FromDishka[IUserServiceUoW]) -> GetUserInfoResponse:
    async with uow:
        user = await uow.users_read.get(event.id)
    return GetUserInfoResponse(id=user.id, username=user.username)


@broker.subscriber("getuserinfolistquery")
@inject
async def on_get_user_info_list(event: GetUserInfoListQuery, uow: FromDishka[IUserServiceUoW]):
    async with uow:
        users = await uow.users_read.get_many(event.ids)
    return GetUserInfoListResponse(users=[GetUserInfoResponse(id=user.id, username=user.username) for user in users])
