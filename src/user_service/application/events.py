from uuid import UUID

from pydantic import ConfigDict

from src.common.message_bus.schemas import Event


class UserCreatedEvent(Event):
    id: UUID
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)
