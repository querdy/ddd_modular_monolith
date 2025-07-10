from dataclasses import dataclass
from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4

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
    def create(cls, name: str, description: str, stages: list[Stage] | None = None) -> Self:
        if stages is None:
            stages = []
        return cls(
            id=uuid4(),
            name=SubprojectName.create(name),
            status=SubprojectStatus.CREATED,
            description=SubprojectDescription.create(description),
            stages=stages,
        )
