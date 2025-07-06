from litestar.dto import DataclassDTO, DTOConfig

from src.user_service.domain.aggregates.role import Role
from src.user_service.presentation.schemas.role import CreateRoleRequestSchema, AssignRoleRequestSchema


class RoleWithPermissionsResponseDTO(DataclassDTO[Role]):
    config = DTOConfig(max_nested_depth=1)


class RoleShortResponseDTO(DataclassDTO[Role]):
    config = DTOConfig(max_nested_depth=0)


class CreateRoleRequestDTO(DataclassDTO[CreateRoleRequestSchema]): ...


class AssignRoleRequestDTO(DataclassDTO[AssignRoleRequestSchema]): ...
