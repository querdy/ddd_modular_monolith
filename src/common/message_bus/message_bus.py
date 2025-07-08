from typing import TypeVar, Type

from faststream.rabbit import RabbitBroker
from pydantic import BaseModel

from src.common.message_bus.schemas import Query, Event

T = TypeVar("T", bound=BaseModel)

class FastStreamMessageBus:
    def __init__(self, broker: RabbitBroker):
        self._broker = broker

    async def publish(self, event: Event) -> None:
        topic = self._resolve_topic(event)
        await self._broker.publish(event, topic)

    async def query(self, query: Query[T], response_model: Type[T]) -> T:
        topic = self._resolve_topic(query)
        msg = await self._broker.request(query.model_dump(), queue=topic)
        data = msg.body
        return response_model.model_validate(data)

    @staticmethod
    def _resolve_topic(message: BaseModel) -> str:
        return f"{message.__class__.__module__}.{message.__class__.__name__}".replace("_", ".").lower()