from dataclasses import dataclass
from uuid import UUID


@dataclass
class ProjectCreateSchema:
    name: str
    description: str | None = None


@dataclass
class ProjectUpdateRequestSchema:
    name: str
    description: str | None = None


@dataclass
class CreateTemplateRequestSchema:
    subproject_id: UUID
