from typing import Self

from src.common.exceptions.domain import DomainError


class MessageText(str):
    MAX_LENGTH = 255

    @classmethod
    def create(cls, value: str) -> Self:
        value = value.strip()
        if not isinstance(value, str):
            raise DomainError(f"{cls.__name__} должен быть строкой")
        if len(value) > cls.MAX_LENGTH:
            raise DomainError(f"Максимальная длина {cls.__name__} {cls.MAX_LENGTH} символов")
        return cls(value)
