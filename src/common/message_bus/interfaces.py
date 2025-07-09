from typing import Protocol, TypeVar, Type
from pydantic import BaseModel

from src.common.message_bus.schemas import Event, Query

T = TypeVar("T", bound=BaseModel)


class IMessageBus(Protocol):
    async def publish(self, event: Event) -> None: ...
    async def query(self, query: Query, response_model: Type[T]) -> T: ...
