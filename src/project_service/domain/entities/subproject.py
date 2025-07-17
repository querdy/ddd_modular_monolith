from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from src.common.exceptions.domain import DomainError
from src.project_service.domain.entities.message import Message
from src.project_service.domain.entities.stage import Stage, StageStatus
from src.project_service.domain.value_objects.enums import SubprojectStatus
from src.project_service.domain.value_objects.stage_description import StageDescription
from src.project_service.domain.value_objects.stage_name import StageName
from src.project_service.domain.value_objects.subproject_description import SubprojectDescription
from src.project_service.domain.value_objects.subproject_name import SubprojectName


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

    def _update_status(self):
        if len(self.stages) == 0:
            self.status = SubprojectStatus.CREATED

        child_statuses = tuple(stage.status for stage in self.stages)

        if all(child_status == StageStatus.COMPLETED for child_status in child_statuses):
            self.status = SubprojectStatus.COMPLETED

        else:
            self.status = SubprojectStatus.IN_PROGRESS

    def add_stage(self, stage: Stage) -> None:
        if next(filter(lambda current_stages: current_stages.name == stage.name, self.stages), None):
            raise DomainError(f"Этап с названием {stage.name} уже существует у данного подпроекта")
        self.stages.append(stage)
        self._update_status()

    def remove_stage(self, stage_id: UUID) -> None:
        stage_to_remove = next(filter(lambda current_stage: current_stage.id == stage_id, self.stages), None)
        if stage_to_remove is None:
            raise DomainError(f"Этап с идентификатором {stage_id} не найден у данного подпроекта")

        self.stages.remove(stage_to_remove)
        self._update_status()

    def update_stage(
        self,
        stage_id: UUID,
        name: str,
        description: str | None = None,
    ) -> Stage:
        stage: Stage | None = next(filter(lambda current_stages: current_stages.id == stage_id, self.stages), None)
        if stage is None:
            raise DomainError(f"Этап с ID {stage_id} не найден")
        stage.update(name, description)
        return stage

    def change_stage_status(self, stage_id: UUID, status: str, message: Message | None) -> Stage:
        stage = next(filter(lambda current_stages: current_stages.id == stage_id, self.stages), None)
        if stage is None:
            raise DomainError(f"Этап с ID {stage_id} не найден")
        stage.change_status(status, message)
        self._update_status()
        return stage

    def update(self, name: str | None = None, description: str | None = None) -> None:
        if name is not None:
            self.name = SubprojectName.create(name)
        if description is not None:
            self.description = SubprojectDescription.create(description)
