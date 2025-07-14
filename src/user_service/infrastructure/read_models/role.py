from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.user_service.infrastructure.read_models.permission import PermissionRead


class RoleRead(BaseModel):
    id: UUID
    name: str
    permissions: list[PermissionRead]

    model_config = ConfigDict(from_attributes=True)
