from typing import Self

from src.common.exceptions.domain import DomainError


class RoleName(str):
    @classmethod
    def create(cls, value: str) -> Self:
        if not value:
            raise DomainError(f"Некорректное название роли: {value}")
        return cls(value)
