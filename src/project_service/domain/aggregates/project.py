from dataclasses import dataclass
from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4

from loguru import logger

from src.common.exceptions.domain import DomainError
from src.project_service.domain.entities.stage import Stage
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.domain.value_objects.project_description import ProjectDescription
from src.project_service.domain.value_objects.project_name import ProjectName


class ProjectStatus(StrEnum):
    CREATED = "Создан"
    COMPLETED = "Завершен"


@dataclass
class Project:
    id: UUID
    name: ProjectName
    description: ProjectDescription | None
    status: ProjectStatus
    subprojects: list[Subproject]

    @classmethod
    def create(cls, name: str, description: str | None = None, subprojects: list[Subproject] | None = None) -> Self:
        if subprojects is None:
            subprojects = []
        return cls(
            id=uuid4(),
            name=ProjectName.create(name),
            status=ProjectStatus.CREATED,
            description=ProjectDescription.create(description) if description else None,
            subprojects=subprojects,
        )

    def add_subproject(self, subproject: Subproject) -> None:
        if next(filter(lambda current_subproject: current_subproject.name == subproject.name, self.subprojects), None):
            raise DomainError(f"Подпроект с названием {subproject.name} уже существует у данного проекта")
        self.subprojects.append(subproject)

    def remove_subproject(self, subproject_id: UUID) -> None:
        subproject_to_remove = next(
            filter(lambda current_subproject: current_subproject.id == subproject_id, self.subprojects), None
        )
        if subproject_to_remove is None:
            raise DomainError(f"Подпроект с идентификатором {subproject_id} не найден у данного проекта")

        self.subprojects.remove(subproject_to_remove)

    def get_subproject_by_id(self, subproject_id: UUID) -> Subproject:
        return next(filter(lambda subproject: subproject.id == subproject_id, self.subprojects), None)

    def get_stage_by_id(self, stage_id: UUID) -> Stage | None:
        for subproject in self.subprojects:
            stage = next((stage for stage in subproject.stages if stage.id == stage_id), None)
            if stage is not None:
                return stage
        return None
