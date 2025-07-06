from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class PermissionDTO:
    code: str
    description: str


@dataclass(frozen=True)
class RoleDTO:
    id: UUID
    name: str
    permissions: list[PermissionDTO]


@dataclass(frozen=True)
class UserRoleAssignmentWithRolesDTO:
    role: RoleDTO
    expires_at: datetime | None


@dataclass(frozen=True)
class UserWithRolesDTO:
    id: UUID
    username: str
    email: str
    role_assignments: list[UserRoleAssignmentWithRolesDTO]
