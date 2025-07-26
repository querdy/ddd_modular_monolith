from litestar.dto import DataclassDTO, DTOConfig
from litestar.plugins.pydantic import PydanticDTO

from src.user_service.domain.aggregates.role import Role
from src.user_service.infrastructure.read_models.role import RoleRead
from src.user_service.presentation.schemas.role import (
    CreateRoleRequestSchema,
    AssignRoleRequestSchema,
    UpdateRoleRequestSchema,
    UnsignRoleRequestSchema,
)


class RoleWithPermissionsResponseDTO(DataclassDTO[Role]):
    config = DTOConfig(max_nested_depth=1)


class RoleShortResponseDTO(DataclassDTO[Role]):
    config = DTOConfig(
        max_nested_depth=0,
        exclude={
            "permission_ids",
        },
    )


class UpdateRoleRequestDTO(DataclassDTO[UpdateRoleRequestSchema]): ...


class CreateRoleRequestDTO(DataclassDTO[CreateRoleRequestSchema]): ...


class AssignRoleRequestDTO(DataclassDTO[AssignRoleRequestSchema]): ...


class UnsignRoleRequestDTO(DataclassDTO[UnsignRoleRequestSchema]): ...
