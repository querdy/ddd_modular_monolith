from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from src.user_service.domain.value_objects.permission_description import PermissionDescription
from src.user_service.domain.value_objects.permission_code import PermissionCode


@dataclass(frozen=True)
class Permission:
    id: UUID
    code: PermissionCode
    description: PermissionDescription

    @classmethod
    def create(cls, code: str, description: str) -> Self:
        return Permission(
            id=uuid4(),
            code=PermissionCode.create(code),
            description=PermissionDescription(description)
        )
