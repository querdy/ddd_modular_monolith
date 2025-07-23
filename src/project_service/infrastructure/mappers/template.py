from functools import singledispatch
from uuid import UUID

from src.project_service.domain.entities.stage_template import StageTemplate
from src.project_service.domain.entities.subproject_template import SubprojectTemplate
from src.project_service.infrastructure.db.postgres.models import SubprojectTemplateModel, StageTemplateModel


@singledispatch
def subproject_template_to_orm(obj, project_id: UUID) -> SubprojectTemplateModel:
    raise NotImplementedError(f"No orm mapper for {type(obj)}")


@singledispatch
def stage_template_to_orm(obj) -> StageTemplateModel:
    raise NotImplementedError(f"No orm mapper for {type(obj)}")


@singledispatch
def subproject_template_to_domain(obj) -> SubprojectTemplate:
    raise NotImplementedError(f"No domain mapper for {type(obj)}")


@singledispatch
def stage_template_to_domain(obj) -> StageTemplate:
    raise NotImplementedError(f"No domain mapper for {type(obj)}")


@subproject_template_to_orm.register
def _(obj: SubprojectTemplate, project_id: UUID) -> SubprojectTemplateModel:
    return SubprojectTemplateModel(
        id=obj.id,
        stages=[stage_template_to_orm(stage) for stage in obj.stages],
    )


@stage_template_to_orm.register
def _(obj: StageTemplate) -> StageTemplateModel:
    return StageTemplateModel(
        id=obj.id,
        name=obj.name,
        description=obj.description,
    )


@subproject_template_to_domain.register
def _(obj: SubprojectTemplateModel) -> SubprojectTemplate:
    return SubprojectTemplate(
        id=obj.id,
        stages=[stage_template_to_domain(stage) for stage in obj.stages],
    )


@stage_template_to_domain.register
def _(obj: StageTemplateModel) -> StageTemplate:
    return StageTemplate(
        id=obj.id,
        name=obj.name,
        description=obj.description,
    )
