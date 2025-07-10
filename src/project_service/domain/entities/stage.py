from dataclasses import dataclass
from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4

from src.project_service.domain.entities.message import Message
from src.project_service.domain.value_objects.stage_description import StageDescription
from src.project_service.domain.value_objects.stage_name import StageName


class StageStatus(StrEnum):
    CREATED = "Создан"
    IN_PROGRESS = "В процессе"
    COMPLETED = "Завершен"
    CONFIRMED = "Подтвержден"


@dataclass
class Stage:
    id: UUID
    name: StageName
    status: StageStatus
    description: StageDescription
    messages: list[Message]

    @classmethod
    def create(cls, name: str, description: str) -> Self:
        return cls(
            id=uuid4(),
            name=StageName.create(name),
            status=StageStatus.CREATED,
            description=StageDescription.create(description),
        )
