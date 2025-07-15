from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from src.user_service.domain.value_objects.role_name import RoleName


@dataclass
class Role:
    id: UUID
    name: RoleName
    permission_ids: list[UUID]

    @classmethod
    def create(cls, name: str) -> Self:
        return Role(id=uuid4(), name=RoleName.create(name), permission_ids=[])

    def add_permission(self, permission_id: UUID):
        if permission_id not in self.permission_ids:
            self.permission_ids.append(permission_id)

    def remove_permission(self, permission_id: UUID):
        if permission_id in self.permission_ids:
            self.permission_ids.remove(permission_id)

    def update(self, name: str, permission_ids: list[UUID]) -> None:
        self.name = RoleName.create(name)
        self.permission_ids = permission_ids