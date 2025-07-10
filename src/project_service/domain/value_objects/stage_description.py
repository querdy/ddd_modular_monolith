from typing import Self

from src.common.exceptions.domain import DomainError


class StageDescription(str):
    @classmethod
    def create(cls, value: str) -> Self:
        if not value:
            raise DomainError(f"Некорректное описание этапа: {value}")
        return cls(value)
