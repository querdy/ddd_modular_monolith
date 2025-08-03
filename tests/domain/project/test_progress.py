from uuid import uuid4

from src.project_service.domain.aggregates.project import Project
from src.project_service.domain.entities.message import Message
from src.project_service.domain.entities.stage import Stage
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.domain.value_objects.enums import ProjectStatus, StageStatus


def test_project_updates_status_on_stage_completion():
    stage = Stage.create("stage")
    sub = Subproject.create("sub", stages=[stage])
    project = Project.create("proj", subprojects=[sub])

    assert project.status == ProjectStatus.CREATED
    assert project.progress == 0.0

    message = Message.create(text="done", author_id=uuid4())
    project.change_stage_status(stage.id, StageStatus.CONFIRMED, message)

    assert project.status == ProjectStatus.IN_PROGRESS
    assert project.progress == 0.0

    project.change_stage_status(stage.id, StageStatus.COMPLETED)

    assert project.status == ProjectStatus.COMPLETED
    assert project.progress == 1.0

    stage = Stage.create("stage")
    sub = Subproject.create("sub2", stages=[stage])
    project.add_subproject(sub)

    assert project.progress == 0.5
    assert project.status == ProjectStatus.IN_PROGRESS

    project.change_stage_status(stage.id, StageStatus.COMPLETED)

    assert project.progress == 1.0
    assert project.status == ProjectStatus.COMPLETED