import re
from typing import Self

from src.common.exceptions.domain import DomainError


class Email(str):
    _EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    @classmethod
    def create(cls, value: str) -> Self:
        value = value.lower().strip()
        if not isinstance(value, str):
            raise DomainError("Email должен быть строкой")
        if not cls._EMAIL_REGEX.match(value):
            raise DomainError("Некорректный формат email")
        return cls(value)
