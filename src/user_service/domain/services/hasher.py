from passlib.context import CryptContext


class Argon2PasswordHasher:
    def __init__(self):
        self._context = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self._context.hash(password)

    def verify(self, plain: str, hashed: str) -> bool:
        return self._context.verify(plain, hashed)
