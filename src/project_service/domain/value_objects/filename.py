from typing import Self

from src.common.exceptions.domain import DomainError


class FileName(str):
    @classmethod
    def create(cls, value: str) -> Self:
        value = value.strip()
        if not isinstance(value, str):
            raise DomainError(f"{cls.__name__} должен быть строкой")
        return cls(value)
