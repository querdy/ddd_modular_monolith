from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MessageRead(BaseModel):
    id: UUID
    created_at: datetime
    author: dict
    text: str
