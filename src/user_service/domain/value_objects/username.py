from typing import Self

from src.common.exceptions.domain import DomainError


class Username(str):
    @classmethod
    def create(cls, value: str) -> Self:
        if not value:
            raise DomainError(f"Некорректный username: {value}")
        return cls(value)
