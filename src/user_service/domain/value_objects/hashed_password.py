from typing import Self

from src.common.exceptions.domain import DomainError
from src.user_service.domain.protocols.hasher import PasswordHasherProtocol
from src.user_service.domain.services.hasher import Argon2PasswordHasher


class HashedPassword(str):
    MIN_LENGTH = 4

    @classmethod
    def create(
        cls,
        plain_password: str,
        hasher: PasswordHasherProtocol = Argon2PasswordHasher(),
    ) -> Self:
        if len(plain_password) < cls.MIN_LENGTH:
            raise DomainError(f"Пароль должен содержать не менее {cls.MIN_LENGTH} символов")
        hashed_password = hasher.hash(plain_password)
        return cls(hashed_password)

    def verify(
        self,
        plain_password: str,
        hasher: PasswordHasherProtocol = Argon2PasswordHasher(),
    ) -> bool:
        """Проверяет хэш пароля"""
        return hasher.verify(plain_password, self)
