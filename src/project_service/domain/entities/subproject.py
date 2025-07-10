from dataclasses import dataclass
from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4

from src.common.exceptions.domain import DomainError
from src.project_service.domain.entities.stage import Stage
from src.project_service.domain.value_objects.subproject_description import SubprojectDescription
from src.project_service.domain.value_objects.subproject_name import SubprojectName


class SubprojectStatus(StrEnum):
    CREATED = "Создан"
    COMPLETED = "Завершен"


@dataclass
class Subproject:
    id: UUID
    name: SubprojectName
    description: SubprojectDescription
    status: SubprojectStatus
    stages: list[Stage]

    @classmethod
    def create(cls, name: str, description: str | None = None, stages: list[Stage] | None = None) -> Self:
        if stages is None:
            stages = []
        return cls(
            id=uuid4(),
            name=SubprojectName.create(name),
            status=SubprojectStatus.CREATED,
            description=SubprojectDescription.create(description) if description else None,
            stages=stages,
        )

    def add_stage(self, stage: Stage) -> None:
        if next(filter(lambda current_stages: current_stages.name == stage.name, self.stages), None):
            raise DomainError(f"Этап с названием {stage.name} уже существует у данного подпроекта")
        self.stages.append(stage)
