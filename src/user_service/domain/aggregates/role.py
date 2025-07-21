from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from src.user_service.domain.enities.permission import Permission
from src.user_service.domain.value_objects.role_name import RoleName


@dataclass(slots=True)
class Role:
    id: UUID
    name: RoleName
    permissions: list[Permission]
    # permission_ids: list[UUID]

    @classmethod
    def create(cls, name: str) -> Self:
        return Role(
            id=uuid4(),
            name=RoleName.create(name),
            permissions=[],
            # permission_ids=[]
        )

    def add_permission(self, permission: Permission):
        if permission not in self.permissions:
            self.permissions.append(permission)

    def remove_permission(self, permission: Permission):
        if permission in self.permissions:
            self.permissions.remove(permission)

    # def add_permission(self, permission_id: UUID):
    #     if permission_id not in self.permission_ids:
    #         self.permission_ids.append(permission_id)
    #
    # def remove_permission(self, permission_id: UUID):
    #     if permission_id in self.permission_ids:
    #         self.permission_ids.remove(permission_id)

    def update(
        self,
        name: str,
        permissions: list[Permission],
        # permission_ids: list[UUID]
    ) -> None:
        self.name = RoleName.create(name)
        self.permissions = permissions
        # self.permission_ids = permission_ids
