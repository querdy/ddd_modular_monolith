from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Self
from uuid import UUID, uuid4

from loguru import logger

from src.common.exceptions.domain import DomainError
from src.project_service.domain.entities.file_attachment import FileAttachment
from src.project_service.domain.entities.message import Message
from src.project_service.domain.entities.stage import Stage, StageStatus
from src.project_service.domain.value_objects.enums import SubprojectStatus
from src.project_service.domain.value_objects.subproject_description import SubprojectDescription
from src.project_service.domain.value_objects.subproject_name import SubprojectName


@dataclass
class Subproject:
    id: UUID
    name: SubprojectName
    description: SubprojectDescription
    created_at: datetime
    updated_at: datetime
    status: SubprojectStatus
    progress: float
    stages: list[Stage]
    files: list[FileAttachment]

    @classmethod
    def create(cls, name: str, description: str | None = None, stages: list[Stage] | None = None) -> Self:
        if stages is None:
            stages = []
        return cls(
            id=uuid4(),
            name=SubprojectName.create(name),
            created_at=datetime.now(UTC).replace(tzinfo=None),
            updated_at=datetime.now(UTC).replace(tzinfo=None),
            status=SubprojectStatus.CREATED,
            description=SubprojectDescription.create(description) if description else None,
            progress=0,
            stages=stages,
            files=[]
        )

    def _update_status(self):
        if len(self.stages) == 0:
            self.status = SubprojectStatus.CREATED

        child_statuses = tuple(stage.status for stage in self.stages)
        if len(child_statuses) == 0:
            self.progress = 0
        else:
            self.progress = child_statuses.count(StageStatus.COMPLETED) / len(child_statuses)

        if all(child_status == StageStatus.COMPLETED for child_status in child_statuses):
            self.status = SubprojectStatus.COMPLETED
        else:
            self.status = SubprojectStatus.IN_PROGRESS

    def add_file(self, filename: str, content_type: str, size: int, path: str) -> None:
        file = FileAttachment.create(
            filename=filename,
            content_type=content_type,
            size=size,
            path=path,
        )
        self.files.append(file)

    def add_file_to_stage(self, stage_id: UUID, filename: str, content_type: str, size: int, path: str) -> None:
        stage = self.get_stage_by_id(stage_id)
        stage.add_file(filename, content_type, size, path)

    def add_stage(self, stage: Stage) -> None:
        if next(filter(lambda current_stages: current_stages.name == stage.name, self.stages), None):
            raise DomainError(f"Этап с названием {stage.name} уже существует у данного подпроекта")
        self.stages.append(stage)
        self._update_status()
        self.updated_at = datetime.now(UTC).replace(tzinfo=None)

    def remove_stage(self, stage_id: UUID) -> None:
        stage_to_remove = self.get_stage_by_id(stage_id)
        self.stages.remove(stage_to_remove)
        self._update_status()
        self.updated_at = datetime.now(UTC).replace(tzinfo=None)

    def update_stage(
        self,
        stage_id: UUID,
        name: str,
        description: str | None = None,
    ) -> Stage:
        stage = self.get_stage_by_id(stage_id)
        stage.update(name, description)
        return stage

    def get_stage_by_id(self, stage_id: UUID) -> Stage:
        stage = next(filter(lambda current_stages: current_stages.id == stage_id, self.stages), None)
        if stage is None:
            raise DomainError(f"Этап с ID {stage_id} не найден")
        return stage

    def change_stage_status(self, stage_id: UUID, status: str, message: Message | None) -> Stage:
        stage = self.get_stage_by_id(stage_id)
        stage.change_status(status, message)
        self._update_status()
        return stage

    def add_message_to_stage(self, stage_id: UUID, message: Message) -> Stage:
        stage = self.get_stage_by_id(stage_id)
        stage.add_message(message)
        return stage

    def update(self, name: str, description: str | None = None) -> None:
        self.name = SubprojectName.create(name)
        if description is not None:
            self.description = SubprojectDescription.create(description)
        self.updated_at = datetime.now(UTC).replace(tzinfo=None)
