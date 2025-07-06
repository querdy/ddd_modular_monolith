from typing import Self

from src.user_service.domain.exceptions import DomainError


class PermissionDescription(str):
    @classmethod
    def create(cls, value: str) -> Self:
        if not value:
            raise DomainError(f"Некорректное описание разрешения: {value}")
        return cls(value)
