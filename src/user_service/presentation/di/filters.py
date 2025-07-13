from typing import Optional, Annotated
from uuid import UUID

from litestar.params import Parameter

from src.user_service.presentation.schemas.permission import FilterPermissionsRequestSchema


async def get_permissions_filters(
    role_id: Annotated[Optional[UUID], Parameter(default=None)],
) -> FilterPermissionsRequestSchema:
    return FilterPermissionsRequestSchema(role_id=role_id)
