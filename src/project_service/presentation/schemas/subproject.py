from dataclasses import dataclass
from uuid import UUID


@dataclass
class SubprojectCreateRequestSchema:
    project_id: UUID
    name: str
    description: str
