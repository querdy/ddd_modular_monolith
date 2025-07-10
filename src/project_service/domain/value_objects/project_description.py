from typing import Self

from src.common.exceptions.domain import DomainError


class ProjectDescription(str):
    @classmethod
    def create(cls, value: str) -> Self:
        if not value:
            raise DomainError(f"Некорректное описание проекта: {value}")
        return cls(value)
