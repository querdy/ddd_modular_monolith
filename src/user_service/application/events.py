from uuid import UUID

from src.common.message_bus.schemas import Event


class UserCreatedEvent(Event):
    id: UUID
    username: str
    email: str
