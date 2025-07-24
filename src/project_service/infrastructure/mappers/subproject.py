from functools import singledispatch

from src.project_service.domain.entities.subproject import Subproject, SubprojectStatus
from src.project_service.domain.value_objects.subproject_description import SubprojectDescription
from src.project_service.domain.value_objects.subproject_name import SubprojectName
from src.project_service.infrastructure.db.postgres.models import SubprojectModel
from src.project_service.infrastructure.mappers.stage import stage_to_orm, stage_to_domain


@singledispatch
def subproject_to_orm(obj) -> SubprojectModel:
    raise NotImplementedError(f"No orm mapper for {type(obj)}")


@subproject_to_orm.register
def _(obj: Subproject) -> SubprojectModel:
    return SubprojectModel(
        id=obj.id,
        name=obj.name,
        description=obj.description,
        created_at=obj.created_at,
        updated_at=obj.updated_at,
        status=obj.status,
        progress=obj.progress,
        stages=[stage_to_orm(stage) for stage in obj.stages],
    )


@singledispatch
def subproject_to_domain(obj) -> Subproject:
    raise NotImplementedError(f"No domain mapper for {type(obj)}")


@subproject_to_domain.register
def _(obj: SubprojectModel) -> Subproject:
    return Subproject(
        id=obj.id,
        name=SubprojectName(obj.name),
        description=SubprojectDescription(obj.description) if obj.description else None,
        created_at=obj.created_at,
        updated_at=obj.updated_at,
        status=SubprojectStatus(obj.status),
        progress=obj.progress,
        stages=[stage_to_domain(stage) for stage in obj.stages],
    )
