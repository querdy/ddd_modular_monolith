from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SubprojectRead(BaseModel):
    id: UUID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    progress: float
    status: str
    project_id: UUID

    model_config = ConfigDict(from_attributes=True)
