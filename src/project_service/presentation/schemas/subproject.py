from dataclasses import dataclass
from uuid import UUID


@dataclass
class SubprojectCreateRequestSchema:
    project_id: UUID
    name: str
    description: str | None = None


@dataclass
class FilterSubprojectRequestSchema:
    project_id: UUID = None
