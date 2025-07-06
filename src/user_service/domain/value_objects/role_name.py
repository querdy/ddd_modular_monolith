from typing import Self

from src.user_service.domain.exceptions import DomainError


class RoleName(str):
    @classmethod
    def create(cls, value: str) -> Self:
        if not value:
            raise DomainError(f"Некорректное название роли: {value}")
        return cls(value)
