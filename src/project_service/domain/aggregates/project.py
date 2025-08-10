from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Self
from uuid import UUID, uuid4

from src.common.exceptions.domain import DomainError
from src.project_service.domain.entities.file_attachment import FileAttachment
from src.project_service.domain.entities.message import Message
from src.project_service.domain.entities.stage import Stage
from src.project_service.domain.entities.subproject import Subproject, SubprojectStatus
from src.project_service.domain.entities.subproject_template import SubprojectTemplate, StageTemplate
from src.project_service.domain.value_objects.enums import ProjectStatus
from src.project_service.domain.value_objects.project_description import ProjectDescription
from src.project_service.domain.value_objects.project_name import ProjectName


@dataclass
class Project:
    id: UUID
    name: ProjectName
    description: ProjectDescription | None
    created_at: datetime
    updated_at: datetime
    status: ProjectStatus
    progress: float
    subprojects: list[Subproject]
    files: list[FileAttachment]

    template: SubprojectTemplate | None = field(default=None)

    @classmethod
    def create(cls, name: str, description: str | None = None, subprojects: list[Subproject] | None = None) -> Self:
        if subprojects is None:
            subprojects = []
        return cls(
            id=uuid4(),
            name=ProjectName.create(name),
            description=ProjectDescription.create(description) if description else None,
            created_at=datetime.now(UTC).replace(tzinfo=None),
            updated_at=datetime.now(UTC).replace(tzinfo=None),
            status=ProjectStatus.CREATED,
            subprojects=subprojects,
            progress=0.0,
            template=None,
            files=[],
        )

    def add_file(self, filename: str, content_type: str, size: int, path: str) -> None:
        file = FileAttachment.create(
            filename=filename,
            content_type=content_type,
            size=size,
            path=path,
        )
        self.files.append(file)

    def add_file_to_subproject(self, subproject_id: UUID, filename: str, content_type: str, size: int, path: str) -> None:
        subproject = self.get_subproject_by_id(subproject_id)
        subproject.add_file(filename, content_type, size, path)

    def add_file_to_stage(self, stage_id: UUID, filename: str, content_type: str, size: int, path: str) -> None:
        subproject_with_stage = self.get_subproject_by_stage_id(stage_id)
        subproject_with_stage.add_file_to_stage(stage_id, filename, content_type, size, path)


    def make_template_from_subproject(self, subproject_id: UUID):
        subproject = self.get_subproject_by_id(subproject_id)
        if self.template is not None:
            self.template.stages = [
                StageTemplate.create(
                    name=stage.name,
                    description=stage.description,
                )
                for stage in subproject.stages
            ]
        else:
            template = SubprojectTemplate.create(
                stages=[
                    StageTemplate.create(
                        name=stage.name,
                        description=stage.description,
                    )
                    for stage in subproject.stages
                ]
            )
            self.template = template

    def _update_status(self):
        if len(self.subprojects) == 0:
            self.status = ProjectStatus.CREATED

        child_statuses = tuple(subproject.status for subproject in self.subprojects)

        if len(child_statuses) == 0:
            self.progress = 0
        else:
            self.progress = child_statuses.count(SubprojectStatus.COMPLETED) / len(child_statuses)

        if all(child_status == SubprojectStatus.COMPLETED for child_status in child_statuses):
            self.status = ProjectStatus.COMPLETED

        else:
            self.status = ProjectStatus.IN_PROGRESS

    def add_subproject(self, subproject: Subproject) -> None:
        if next(filter(lambda current_subproject: current_subproject.name == subproject.name, self.subprojects), None):
            raise DomainError(f"Подпроект с названием {subproject.name} уже существует у данного проекта")
        self.subprojects.append(subproject)
        self._update_status()
        self.updated_at = datetime.now(UTC).replace(tzinfo=None)

    def remove_subproject(self, subproject_id: UUID) -> None:
        subproject_to_remove = next(
            filter(lambda current_subproject: current_subproject.id == subproject_id, self.subprojects), None
        )
        if subproject_to_remove is None:
            raise DomainError(f"Подпроект с идентификатором {subproject_id} не найден у данного проекта")

        self.subprojects.remove(subproject_to_remove)
        self._update_status()
        self.updated_at = datetime.now(UTC).replace(tzinfo=None)

    def get_subproject_by_id(self, subproject_id: UUID) -> Subproject:
        subproject =  next(filter(lambda sp: sp.id == subproject_id, self.subprojects), None)
        if subproject is None:
            raise DomainError(f"Подпроект с id `{subproject_id}` не найден")
        return subproject

    def get_stage_by_id(self, stage_id: UUID) -> Stage | None:
        for subproject in self.subprojects:
            stage = next((stage for stage in subproject.stages if stage.id == stage_id), None)
            if stage is not None:
                return stage

    def get_subproject_by_stage_id(self, stage_id: UUID) -> Subproject | None:
        return next(filter(lambda sp: any(stage.id == stage_id for stage in sp.stages), self.subprojects), None)

    def update(self, name: str, description: str | None = None) -> None:
        self.name = ProjectName.create(name)
        if description is not None:
            self.description = ProjectDescription.create(description)
        self.updated_at = datetime.now(UTC).replace(tzinfo=None)

    def update_stage(
        self,
        stage_id: UUID,
        name: str,
        description: str | None = None,
    ) -> Stage:
        subproject_with_stage = self.get_subproject_by_stage_id(stage_id)
        if subproject_with_stage is None:
            raise DomainError(f"Подпроект с этапом {stage_id} не найден")
        stage = subproject_with_stage.update_stage(stage_id, name, description)
        return stage

    def change_stage_status(self, stage_id: UUID, status: str, message: Message | None = None) -> Stage:
        subproject_with_stage = self.get_subproject_by_stage_id(stage_id)
        if subproject_with_stage is None:
            raise DomainError(f"Подпроект с этапом {stage_id} не найден")
        stage = subproject_with_stage.change_stage_status(stage_id, status, message)
        self._update_status()
        return stage

    def add_message_to_stage(self, stage_id: UUID, message: Message) -> Stage:
        subproject_with_stage = self.get_subproject_by_stage_id(stage_id)
        if subproject_with_stage is None:
            raise DomainError(f"Подпроект с этапом {stage_id} не найден")
        stage = subproject_with_stage.add_message_to_stage(stage_id, message)
        return stage

    def remove_stage(self, stage_id: UUID) -> None:
        subproject_with_stage = self.get_subproject_by_stage_id(stage_id)
        subproject_with_stage.remove_stage(stage_id)
        self._update_status()
        self.updated_at = datetime.now(UTC).replace(tzinfo=None)

    def update_subproject(
        self,
        subproject_id: UUID,
        name: str,
        description: str | None = None,
    ) -> Subproject:
        subproject: Subproject = next(filter(lambda sp: sp.id == subproject_id, self.subprojects), None)
        subproject.update(name, description)
        return subproject
