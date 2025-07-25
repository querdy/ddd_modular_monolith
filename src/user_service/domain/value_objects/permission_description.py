from typing import Self

from src.common.exceptions.domain import DomainError


class PermissionDescription(str):
    @classmethod
    def create(cls, value: str) -> Self:
        if not value:
            raise DomainError(f"Некорректное описание разрешения: {value}")
        return cls(value)
