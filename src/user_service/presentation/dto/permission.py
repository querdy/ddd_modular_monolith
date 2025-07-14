from litestar.dto import DataclassDTO

from src.user_service.presentation.schemas.permission import CreatePermissionRequestSchema


class CreatePermissionRequestDTO(DataclassDTO[CreatePermissionRequestSchema]): ...
