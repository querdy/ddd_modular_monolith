from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class SubprojectCreateRequestSchema:
    project_id: UUID
    name: str
    description: str | None = field(default=None)
    from_template: bool = field(default=False)


@dataclass
class FilterSubprojectsRequestSchema:
    project_id: UUID = None


@dataclass
class SubprojectUpdateRequestSchema:
    name: str
    description: str | None = None
