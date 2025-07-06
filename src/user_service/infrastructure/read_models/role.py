from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.user_service.domain.value_objects.role_name import RoleName


class PermissionRead(BaseModel):
    id: UUID
    code: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class RoleRead(BaseModel):
    id: UUID
    name: str
    permissions: list[PermissionRead]

    model_config = ConfigDict(from_attributes=True)
