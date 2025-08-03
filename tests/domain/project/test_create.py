from src.project_service.domain.aggregates.project import Project
from src.project_service.domain.value_objects.enums import ProjectStatus

def test_create_project_sets_initial_values():
    project = Project.create(name="My Project", description="Описание")

    assert project.name == "My Project"
    assert project.description == "Описание"
    assert project.status == ProjectStatus.CREATED
    assert project.subprojects == []
    assert project.progress == 0.0