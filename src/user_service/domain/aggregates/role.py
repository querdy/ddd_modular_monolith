from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from src.user_service.domain.enities.permission import Permission
from src.user_service.domain.value_objects.role_name import RoleName


@dataclass
class Role:
    id: UUID
    name: RoleName
    permissions: list[Permission]

    @classmethod
    def create(cls, name: str, permissions: list[Permission]) -> Self:
        return Role(id=uuid4(), name=RoleName.create(name), permissions=permissions)

    def add_permission(self, permission: Permission):
        if permission not in self.permissions:
            self.permissions.append(permission)

    def remove_permission(self, permission: Permission):
        if permission in self.permissions:
            self.permissions.remove(permission)