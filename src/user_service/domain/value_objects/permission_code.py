import re
from typing import Self

from src.user_service.domain.exceptions import DomainError


class PermissionCode(str):
    @classmethod
    def create(cls, value: str) -> Self:
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*:[a-zA-Z_][a-zA-Z0-9_]*$"
        if not value or not re.match(pattern, value):
            raise DomainError(f"Некорректный код разрешения: {value}")
        return cls(value)
