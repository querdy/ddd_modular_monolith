from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.project_service.infrastructure.read_models.file_attachment import FileAttachmentRead
from src.project_service.infrastructure.read_models.message import MessageRead


class StageRead(BaseModel):
    id: UUID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    status: str
    files: list[FileAttachmentRead]
    messages: list[MessageRead]
