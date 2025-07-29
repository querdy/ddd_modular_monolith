from functools import singledispatch

from src.project_service.domain.entities.stage_status_history import StageStatusHistory
from src.project_service.domain.value_objects.enums import StageStatus
from src.project_service.infrastructure.db.postgres.models import StageStatusHistoryModel


@singledispatch
def stage_status_history_to_orm(obj) -> StageStatusHistoryModel:
    raise NotImplementedError(f"No orm mapper for {type(obj)}")


@stage_status_history_to_orm.register
def _(obj: StageStatusHistory) -> StageStatusHistoryModel:
    return StageStatusHistoryModel(
        id=obj.id,
        stage_id=obj.stage_id,
        to_status=obj.to_status,
        changed_by=obj.changed_by,
        changed_at=obj.changed_at,
    )


@singledispatch
def stage_status_history_to_domain(obj) -> StageStatusHistory:
    raise NotImplementedError(f"No domain mapper for {type(obj)}")


@stage_status_history_to_domain.register
def _(obj: StageStatusHistoryModel) -> StageStatusHistory:
    return StageStatusHistory(
        id=obj.id,
        stage_id=obj.stage_id,
        to_status=StageStatus(obj.to_status),
        changed_by=obj.changed_by,
        changed_at=obj.changed_at,
    )
