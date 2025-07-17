from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Self
from uuid import UUID, uuid4

from src.project_service.domain.value_objects.message_text import MessageText


@dataclass
class Message:
    id: UUID
    created_at: datetime
    author_id: UUID
    text: MessageText

    @classmethod
    def create(cls, author_id: UUID, text: str) -> Self:
        return cls(
            id=uuid4(),
            created_at=datetime.now(UTC).replace(tzinfo=None),
            author_id=author_id,
            text=MessageText.create(text),
        )
