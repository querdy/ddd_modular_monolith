from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC
from typing import Self
from uuid import UUID, uuid4

from src.user_service.domain.enities.user_role_assignment import UserRoleAssignment
from src.user_service.domain.exceptions import DomainError
from src.user_service.domain.value_objects.email import Email
from src.user_service.domain.value_objects.hashed_password import HashedPassword
from src.user_service.domain.value_objects.username import Username


@dataclass
class User:
    id: UUID
    username: Username
    email: Email
    hashed_password: HashedPassword
    role_assignments: list[UserRoleAssignment]

    @classmethod
    def create(cls, username: str, email: str, password: str, role_assignment: UserRoleAssignment) -> Self:
        return cls(
            id=uuid4(),
            username=Username(username),
            email=Email(email),
            hashed_password=HashedPassword.create(password),
            role_assignments=[role_assignment],
        )

    def assign_role(self, role_id: UUID, days: int | None = None):
        now = datetime.now(UTC).replace(tzinfo=None)
        expires_at = now + timedelta(days=days) if days else None
        self.role_assignments.append(
            UserRoleAssignment.create(role_id=role_id, expires_at=expires_at)
        )

    def remove_role(self, role_id: UUID) -> None:
        initial_count = len(self.role_assignments)
        if initial_count == 1:
            raise DomainError(f"Нельзя удалить единственную роль у пользователя {self.id}")
        self.role_assignments = [
            assignment for assignment in self.role_assignments if assignment.role_id != role_id
        ]
        if len(self.role_assignments) == initial_count:
            raise DomainError(f"Роль {role_id} не найдена у пользователя {self.id}")
