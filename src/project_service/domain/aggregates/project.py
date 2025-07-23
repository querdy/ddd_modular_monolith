from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Self
from uuid import UUID, uuid4

from loguru import logger

from src.common.exceptions.domain import DomainError
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
    subprojects: list[Subproject]

    template: SubprojectTemplate | None = None

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
            template=None,
        )

    def make_template_from_subproject(self, subproject_id: UUID = UUID("8c9480f4-eefb-427a-8ac8-bb42e5840fbc")):
        subproject = self.get_subproject_by_id(subproject_id)
        template = SubprojectTemplate.create(
            stages=[
                StageTemplate.create(
                    name=stage.name,
                    description=stage.description,
                )
                for stage in subproject.stages
            ]
        )
        logger.info(template)
        self.template = template

    def _update_status(self):
        if len(self.subprojects) == 0:
            self.status = ProjectStatus.CREATED

        child_statuses = tuple(subproject.status for subproject in self.subprojects)

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
        return next(filter(lambda sp: sp.id == subproject_id, self.subprojects), None)

    def get_stage_by_id(self, stage_id: UUID) -> Stage | None:
        for subproject in self.subprojects:
            stage = next((stage for stage in subproject.stages if stage.id == stage_id), None)
            if stage is not None:
                return stage
        return None

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

    def change_stage_status(self, stage_id: UUID, status: str, message: Message | None) -> Stage:
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
