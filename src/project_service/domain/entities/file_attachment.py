from dataclasses import dataclass
from datetime import datetime
from typing import Self
from uuid import UUID, uuid4


@dataclass
class FileAttachment:
    id: UUID
    filename: str
    content_type: str
    size: int
    uploaded_at: datetime
    object_key: str

    @classmethod
    def create(cls) -> Self:
        return cls(id=uuid4(), )