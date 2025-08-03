import pytest

from src.common.exceptions.domain import DomainError
from src.project_service.domain.aggregates.project import Project
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.domain.value_objects.enums import ProjectStatus


def test_add_subproject_appends_and_updates_status():
    project = Project.create("Test")

    project.add_subproject(Subproject.create("sub1"))

    assert len(project.subprojects) == 1
    assert project.status == ProjectStatus.IN_PROGRESS

    project.add_subproject(Subproject.create("sub2"))
    assert len(project.subprojects) == 2
    assert project.status == ProjectStatus.IN_PROGRESS

def test_add_subproject_with_duplicate_name_raises_error():
    project = Project.create("Test")
    sub1 = Subproject.create("sub")
    sub2 = Subproject.create("sub")

    project.add_subproject(sub1)

    with pytest.raises(DomainError, match="уже существует"):
        project.add_subproject(sub2)