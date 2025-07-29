from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict

from src.common.message_bus.schemas import Event


class StageStatusChangedEvent(Event):
    stage_id: UUID
    to_status: str
    changed_by: UUID
    changed_at: datetime

    model_config = ConfigDict(from_attributes=True)
