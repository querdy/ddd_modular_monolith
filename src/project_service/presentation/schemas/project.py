from dataclasses import dataclass


@dataclass
class ProjectCreateSchema:
    name: str
    description: str
