from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from src.project_service.domain.entities.stage_template import StageTemplate


@dataclass
class SubprojectTemplate:
    id: UUID
    stages: list[StageTemplate]

    @classmethod
    def create(cls, stages: list[StageTemplate]) -> Self:
        return cls(
            id=uuid4(),
            stages=stages,
        )
