from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.project_service.infrastructure.read_models.message import MessageRead


@dataclass
class StageRead:
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    status: str
    messages: list[MessageRead]
