from uuid import UUID

from pydantic import BaseModel, ConfigDict


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
