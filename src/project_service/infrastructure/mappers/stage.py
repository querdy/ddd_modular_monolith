from functools import singledispatch

from src.project_service.domain.entities.stage import Stage, StageStatus
from src.project_service.domain.value_objects.stage_description import StageDescription
from src.project_service.domain.value_objects.stage_name import StageName
from src.project_service.infrastructure.db.postgres.models import StageModel
from src.project_service.infrastructure.mappers.message import message_to_orm, message_to_domain
from src.project_service.infrastructure.mappers.stage_files import stage_file_to_orm, stage_file_to_domain


@singledispatch
def stage_to_orm(obj) -> StageModel:
    raise NotImplementedError(f"No orm mapper for {type(obj)}")


@stage_to_orm.register
def _(obj: Stage) -> StageModel:
    return StageModel(
        id=obj.id,
        name=obj.name,
        description=obj.description,
        created_at=obj.created_at,
        updated_at=obj.updated_at,
        status=obj.status,
        files=[stage_file_to_orm(file) for file in obj.files],
        messages=[message_to_orm(message) for message in obj.messages],

    )


@singledispatch
def stage_to_domain(obj) -> Stage:
    raise NotImplementedError(f"No domain mapper for {type(obj)}")


@stage_to_domain.register
def _(obj: StageModel) -> Stage:
    return Stage(
        id=obj.id,
        name=StageName(obj.name),
        description=StageDescription(obj.description) if obj.description else None,
        created_at=obj.created_at,
        updated_at=obj.updated_at,
        status=StageStatus(obj.status),
        files=[stage_file_to_domain(file) for file in obj.files],
        messages=[message_to_domain(message) for message in obj.messages],
    )
