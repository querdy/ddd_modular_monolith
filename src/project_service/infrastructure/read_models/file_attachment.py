from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class FileAttachmentRead(BaseModel):
    id: UUID
    filename: str
    content_type: str
    size: int
    uploaded_at: datetime
    path: str