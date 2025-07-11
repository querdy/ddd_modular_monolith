from typing import Optional
from uuid import UUID

from litestar.params import Parameter

from src.project_service.presentation.schemas.stage import FilterStageRequestSchema
from src.project_service.presentation.schemas.subproject import FilterSubprojectRequestSchema


async def get_subproject_filters(project_id: Optional[UUID] = Parameter(default=None)) -> FilterSubprojectRequestSchema:
    return FilterSubprojectRequestSchema(project_id=project_id)


async def get_stage_filters(subproject_id: Optional[UUID] = Parameter(default=None)) -> FilterStageRequestSchema:
    return FilterStageRequestSchema(subproject_id=subproject_id)
