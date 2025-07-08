from loguru import logger

from src.common.message_bus.broker import broker
from src.user_service.application.events import UserCreatedEvent
from src.user_service.application.use_cases.queries import GetInfoQuery, GetInfoResponse


@broker.subscriber("usercreatedevent")
async def on_user_created(event: UserCreatedEvent):
    logger.info(event)

@broker.subscriber("getinfoquery")
async def on_get_info(event: GetInfoQuery):
    return GetInfoResponse(id=event.user_id, name='kekw')