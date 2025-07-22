from uuid import UUID

from pydantic import ConfigDict

from src.common.message_bus.schemas import Event


class ProjectCreatedEvent(Event):
    id: UUID
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)
