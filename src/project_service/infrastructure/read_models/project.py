from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.project_service.infrastructure.read_models.template import SubprojectTemplateRead


class ProjectRead(BaseModel):
    id: UUID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    status: str
    progress: float
    # subprojects: list[SubprojectRead]
    template: SubprojectTemplateRead | None

    model_config = ConfigDict(from_attributes=True)
