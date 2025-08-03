from functools import singledispatch

from src.project_service.domain.aggregates.project import Project, ProjectStatus
from src.project_service.domain.value_objects.project_description import ProjectDescription
from src.project_service.domain.value_objects.project_name import ProjectName
from src.project_service.infrastructure.db.postgres.models import ProjectModel
from src.project_service.infrastructure.mappers.project_files import project_file_to_orm, project_file_to_domain
from src.project_service.infrastructure.mappers.subproject import subproject_to_orm, subproject_to_domain
from src.project_service.infrastructure.mappers.template import (
    subproject_template_to_orm,
    subproject_template_to_domain,
)


@singledispatch
def project_to_orm(obj) -> ProjectModel:
    raise NotImplementedError(f"No orm mapper for {type(obj)}")


@project_to_orm.register
def _(obj: Project) -> ProjectModel:
    return ProjectModel(
        id=obj.id,
        name=obj.name,
        description=obj.description,
        created_at=obj.created_at,
        updated_at=obj.updated_at,
        status=obj.status,
        progress=obj.progress,
        files=[project_file_to_orm(file) for file in obj.files],
        subprojects=[subproject_to_orm(subproject) for subproject in obj.subprojects],
        template=subproject_template_to_orm(obj.template, obj.id) if obj.template else None,
    )


@singledispatch
def project_to_domain(obj) -> Project:
    raise NotImplementedError(f"No domain mapper for {type(obj)}")


@project_to_domain.register
def _(obj: ProjectModel) -> Project:
    return Project(
        id=obj.id,
        name=ProjectName(obj.name),
        description=ProjectDescription(obj.description) if obj.description else None,
        created_at=obj.created_at,
        updated_at=obj.updated_at,
        status=ProjectStatus(obj.status),
        progress=obj.progress,
        files=[project_file_to_domain(file) for file in obj.files],
        subprojects=[subproject_to_domain(subproject) for subproject in obj.subprojects],
        template=subproject_template_to_domain(obj.template) if obj.template else None,
    )
