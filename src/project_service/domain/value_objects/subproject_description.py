from typing import Self

from src.common.exceptions.domain import DomainError


class SubprojectDescription(str):
    @classmethod
    def create(cls, value: str) -> Self:
        if not value:
            raise DomainError(f"Некорректное описание подпроекта: {value}")
        return cls(value)
