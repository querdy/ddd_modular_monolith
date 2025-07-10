from dataclasses import dataclass
from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4

from src.common.exceptions.domain import DomainError
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
    def create(cls, name: str, description: str, subprojects: list[Subproject] | None = None) -> Self:
        if subprojects is None:
            subprojects = []
        return cls(
            id=uuid4(),
            name=ProjectName.create(name),
            status=ProjectStatus.CREATED,
            description=ProjectDescription.create(description),
            subprojects=subprojects,
        )

    def add_subproject(self, subproject: Subproject) -> None:
        for current_subproject in self.subprojects:
            if current_subproject.name == subproject.name:
                raise DomainError(f"Подпроект с названием {subproject.name} уже существует у данного проекта")
        self.subprojects.append(subproject)

    def get_subproject_by_id(self, subproject_id: UUID) -> Subproject:
        return next(filter(lambda subproject: subproject.id == subproject_id, self.subprojects), None)