from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.user_service.infrastructure.read_models.role import RoleRead


class UserRoleAssignmentRead(BaseModel):
    role: RoleRead
    assigned_at: datetime
    expires_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: UUID
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
    role_assignments: list[UserRoleAssignmentRead]

    model_config = ConfigDict(from_attributes=True)
