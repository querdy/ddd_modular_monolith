from typing import Self

from src.user_service.domain.exceptions import DomainError


class PermissionCode(str):
    @classmethod
    def create(cls, value: str) -> Self:
        if not value or not value.isidentifier():
            raise DomainError(f"Некорректный код разрешения: {value}")
        return cls(value)
