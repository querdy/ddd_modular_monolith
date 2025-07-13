from dataclasses import dataclass
from uuid import UUID

from src.project_service.domain.entities.stage import StageStatus


@dataclass
class StageCreateRequestSchema:
    subproject_id: UUID
    name: str
    description: str | None = None


@dataclass
class FilterStageRequestSchema:
    subproject_id: UUID = None


@dataclass
class StageUpdateRequestSchema:
    name: str | None = None
    description: str | None = None
    status: StageStatus | None = None
