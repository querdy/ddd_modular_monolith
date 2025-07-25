from dataclasses import dataclass
from datetime import datetime, timedelta, UTC
from typing import Self
from uuid import UUID, uuid4

from loguru import logger

from src.user_service.domain.enities.user_role_assignment import UserRoleAssignment
from src.common.exceptions.domain import DomainError
from src.user_service.domain.value_objects.email import Email
from src.user_service.domain.value_objects.hashed_password import HashedPassword
from src.user_service.domain.value_objects.username import Username


@dataclass(slots=True)
class User:
    id: UUID
    username: Username
    email: Email
    hashed_password: HashedPassword
    role_assignments: list[UserRoleAssignment]

    @classmethod
    def create(
        cls,
        username: str,
        email: str,
        password: str,
        repeat_password: str,
        role_assignment: UserRoleAssignment,
    ) -> Self:
        if password != repeat_password:
            raise DomainError(f"Пароль и повтор пароля не совпадают")
        return cls(
            id=uuid4(),
            username=Username(username),
            email=Email(email),
            hashed_password=HashedPassword.create(password),
            role_assignments=[role_assignment],
        )

    def assign_role(self, role_id: UUID, days: int | None = None):
        now = datetime.now(UTC).replace(tzinfo=None, microsecond=0)
        expires_at = now + timedelta(days=days) if days else None

        for assignment in self.role_assignments:
            if assignment.role_id == role_id:
                if assignment.expires_at is None:
                    if days is None:
                        raise DomainError(f"Роль {role_id} уже назначена пользователю бессрочно")
                    count_permanent = sum(1 for assignment in self.role_assignments if assignment.expires_at is None)
                    if count_permanent == 1:
                        raise DomainError("Нельзя заменить последнюю бессрочную роль на временную")
                    assignment.expires_at = expires_at
                    return
                assignment.expires_at = expires_at
                return

        if expires_at is not None:
            if not any(assignment.expires_at is None for assignment in self.role_assignments):
                raise DomainError("Нельзя создать временную роль, если нет ни одной бессрочной")

        self.role_assignments.append(UserRoleAssignment.create(role_id=role_id, expires_at=expires_at))

    def remove_role(self, role_id: UUID) -> None:
        initial_count = len(self.role_assignments)
        if initial_count == 1:
            raise DomainError(f"Нельзя удалить единственную роль у пользователя {self.id}")
        self.role_assignments = [assignment for assignment in self.role_assignments if assignment.role_id != role_id]
        if len(self.role_assignments) == initial_count:
            raise DomainError(f"Роль {role_id} не найдена у пользователя {self.id}")

    def change_password(self, old_password: str, new_password: str, repeat_password: str) -> Self:
        if not self.hashed_password.verify(old_password):
            raise DomainError(f"Указан неверный старый пароль")
        if new_password != repeat_password:
            raise DomainError(f"Пароли не совпадают")
        if old_password == new_password:
            raise DomainError(f"Введены одинаковые старый и новый пароли")
        self.hashed_password = HashedPassword.create(new_password)
