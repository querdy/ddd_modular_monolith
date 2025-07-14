from dataclasses import dataclass
from uuid import UUID

from pydantic import Field


@dataclass
class FilterPermissionsRequestSchema:
    role_id: UUID | None = Field(default=None)


@dataclass
class CreatePermissionRequestSchema:
    code: str
    description: str
