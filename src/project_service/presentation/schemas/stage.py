from dataclasses import dataclass
from uuid import UUID


@dataclass
class StageCreateRequestSchema:
    subproject_id: UUID
    name: str
    description: str | None = None
