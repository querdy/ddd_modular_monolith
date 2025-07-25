from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProjectRead(BaseModel):
    id: UUID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    status: str
    progress: float

    model_config = ConfigDict(from_attributes=True)