from dataclasses import dataclass


@dataclass
class ProjectCreateSchema:
    name: str
    description: str | None = None


@dataclass
class ProjectUpdateRequestSchema:
    name: str | None = None
    description: str | None = None
