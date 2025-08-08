from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Self
from uuid import UUID, uuid4

from src.common.exceptions.domain import DomainError
from src.project_service.domain.entities.file_attachment import FileAttachment
from src.project_service.domain.entities.message import Message
from src.project_service.domain.value_objects.enums import StageStatus
from src.project_service.domain.value_objects.stage_description import StageDescription
from src.project_service.domain.value_objects.stage_name import StageName


@dataclass
class Stage:
    id: UUID
    name: StageName
    description: StageDescription
    created_at: datetime
    updated_at: datetime
    status: StageStatus
    files: list[FileAttachment]

    messages: list[Message]


    @classmethod
    def create(cls, name: str, description: str | None = None) -> Self:
        return cls(
            id=uuid4(),
            name=StageName.create(name),
            created_at=datetime.now(UTC).replace(tzinfo=None),
            updated_at=datetime.now(UTC).replace(tzinfo=None),
            status=StageStatus.CREATED,
            description=StageDescription.create(description) if description else None,
            messages=[],
            files=[]
        )

    def update(self, name: str, description: str | None = None) -> None:
        self.name = StageName.create(name)
        self.description = StageDescription.create(description) if description else None
        self.updated_at = datetime.now(UTC).replace(tzinfo=None)

    def add_file(self, filename: str, content_type: str, size: int, path: str) -> None:
        file = FileAttachment.create(
            filename=filename,
            content_type=content_type,
            size=size,
            path=path,
        )
        self.files.append(file)

    def change_status(self, status: str, message: Message | None = None) -> None:
        if status in (StageStatus.CREATED,):
            raise DomainError(f"Нельзя вручную установить статус `{status}`")
        if status == StageStatus.CONFIRMED and message is None:
            raise DomainError(f"Нельзя установить статус `{status}` без сообщения")
        if message is not None:
            if not isinstance(message, Message):
                raise DomainError(f"Передан некорректный объект сообщения")
            self.messages.append(message)
        if self.status == status:
            raise DomainError(f"Новый статус должен отличаться от установленного")
        self.status = StageStatus(status)
        self.updated_at = datetime.now(UTC).replace(tzinfo=None)

    def add_message(self, message: Message) -> None:
        if not isinstance(message, Message):
            raise DomainError(f"Передан некорректный объект сообщения")
        self.messages.append(message)
