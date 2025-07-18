from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class MessageRead:
    id: UUID
    created_at: datetime
    author: dict
    text: str
