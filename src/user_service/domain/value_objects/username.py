from typing import Self

from src.user_service.domain.exceptions import DomainError


class Username(str):
    @classmethod
    def create(cls, value: str) -> Self:
        if not value:
            raise DomainError(f"Некорректный username: {value}")
        return cls(value)
