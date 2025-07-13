from dataclasses import dataclass
from uuid import UUID


@dataclass
class SubprojectCreateRequestSchema:
    project_id: UUID
    name: str
    description: str | None = None


@dataclass
class FilterSubprojectsRequestSchema:
    project_id: UUID = None


@dataclass
class SubprojectUpdateRequestSchema:
    name: str | None = None
    description: str | None = None
