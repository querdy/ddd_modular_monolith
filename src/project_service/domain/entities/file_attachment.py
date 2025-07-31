from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Self
from uuid import UUID, uuid4

from src.project_service.domain.value_objects.filename import FileName


@dataclass
class FileAttachment:
    id: UUID
    filename: FileName
    content_type: str
    size: int
    uploaded_at: datetime
    object_key: str

    @classmethod
    def create(cls, filename: str, content_type: str, size: int, object_key: str) -> Self:
        return cls(
            id=uuid4(),
            uploaded_at=datetime.now(UTC).replace(tzinfo=None),
            filename=FileName.create(filename),
            content_type=content_type,
            size=size,
            object_key=object_key,
        )
