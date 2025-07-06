from typing import Protocol


class PasswordHasherProtocol(Protocol):
    """Интерфейс для хеширования паролей."""

    def hash(self, password: str) -> str: ...
    def verify(self, plain: str, hashed: str) -> bool: ...
