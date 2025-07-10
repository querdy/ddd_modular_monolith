from functools import singledispatch

from src.project_service.domain.entities.stage import Stage, StageStatus
from src.project_service.domain.value_objects.stage_description import StageDescription
from src.project_service.domain.value_objects.stage_name import StageName
from src.project_service.infrastructure.db.postgres.models import StageModel


@singledispatch
def stage_to_orm(obj) -> StageModel:
    raise NotImplementedError(f"No orm mapper for {type(obj)}")


@stage_to_orm.register
def _(obj: Stage) -> StageModel:
    return StageModel(id=obj.id, name=obj.name, description=obj.description, status=obj.status)


@singledispatch
def stage_to_domain(obj) -> Stage:
    raise NotImplementedError(f"No domain mapper for {type(obj)}")


@stage_to_domain.register
def _(obj: StageModel) -> Stage:
    return Stage(
        id=obj.id,
        name=StageName(obj.name),
        description=StageDescription(obj.description),
        status=StageStatus(obj.status),
        messages=[],
    )
