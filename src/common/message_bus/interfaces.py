from typing import Protocol, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class IMessageBus(Protocol):
    async def publish(self, event: Event) -> None: ...
    async def query(self, query: Query[T], response_model: Type[T]) -> T: ...