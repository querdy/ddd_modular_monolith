from functools import singledispatch

from src.project_service.domain.aggregates.project import Project, ProjectStatus
from src.project_service.domain.value_objects.project_description import ProjectDescription
from src.project_service.domain.value_objects.project_name import ProjectName
from src.project_service.infrastructure.db.postgres.models import ProjectModel
from src.project_service.infrastructure.mappers.subproject import subproject_to_orm, subproject_to_domain


@singledispatch
def project_to_orm(obj) -> ProjectModel:
    raise NotImplementedError(f"No orm mapper for {type(obj)}")


@project_to_orm.register
def _(obj: Project) -> ProjectModel:
    return ProjectModel(
        id=obj.id,
        name=obj.name,
        description=obj.description,
        status=obj.status,
        subprojects=[subproject_to_orm(subproject) for subproject in obj.subprojects],
    )


@singledispatch
def project_to_domain(obj) -> Project:
    raise NotImplementedError(f"No domain mapper for {type(obj)}")


@project_to_domain.register
def _(obj: ProjectModel) -> Project:
    return Project(
        id=obj.id,
        name=ProjectName(obj.name),
        description=ProjectDescription(obj.description),
        status=ProjectStatus(obj.status),
        subprojects=[subproject_to_domain(subproject) for subproject in obj.subprojects],
    )
