from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from src.project_service.domain.value_objects.stage_description import StageDescription
from src.project_service.domain.value_objects.stage_name import StageName


@dataclass
class StageTemplate:
    id: UUID
    name: str
    description: str | None

    @classmethod
    def create(cls, name: str, description: str | None = None) -> Self:
        return cls(
            id=uuid4(),
            name=StageName(name),
            description=StageDescription(description) if description else None,
        )
