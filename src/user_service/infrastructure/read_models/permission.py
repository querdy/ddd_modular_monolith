from uuid import UUID

from pydantic import ConfigDict, BaseModel


class PermissionRead(BaseModel):
    id: UUID
    code: str
    description: str

    model_config = ConfigDict(from_attributes=True)
