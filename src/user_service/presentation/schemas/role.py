from dataclasses import dataclass
from uuid import UUID


@dataclass
class PermissionResponseSchema:
    code: str
    description: str


@dataclass
class AssignRoleRequestSchema:
    role_id: UUID
    term: int = None


@dataclass
class CreateRoleRequestSchema:
    name: str

@dataclass
class UpdateRoleRequestSchema:
    name: str
    permission_ids: list[UUID]