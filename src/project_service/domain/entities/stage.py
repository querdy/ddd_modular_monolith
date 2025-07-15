from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from src.common.exceptions.domain import DomainError
from src.project_service.domain.entities.message import Message
from src.project_service.domain.value_objects.enums import StageStatus
from src.project_service.domain.value_objects.stage_description import StageDescription
from src.project_service.domain.value_objects.stage_name import StageName


@dataclass
class Stage:
    id: UUID
    name: StageName
    description: StageDescription
    status: StageStatus
    messages: list[Message]

    @classmethod
    def create(cls, name: str, description: str | None = None) -> Self:
        return cls(
            id=uuid4(),
            name=StageName.create(name),
            status=StageStatus.CREATED,
            description=StageDescription.create(description) if description else None,
            messages=[],
        )

    def update(self, name: str | None = None, description: str | None = None, status: str | None = None) -> None:
        if name is not None:
            self.name = StageName.create(name)
        if description is not None:
            self.description = StageDescription.create(description)
        if status is not None:
            self.status = StageStatus(status)

    def change_status(self, status: str, message: Message | None = None) -> None:
        if status == StageStatus.CONFIRMED and message is None:
            raise DomainError(f"Нельзя установить статус {status} без сообщения")
        if message is not None:
            if not isinstance(message, Message):
                raise DomainError(f"Передан некорректный объект сообщения")
            self.messages.append(message)
        self.status = StageStatus(status)
