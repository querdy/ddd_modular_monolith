from dataclasses import dataclass, asdict
from datetime import timedelta, datetime, UTC
from typing import Literal
from uuid import UUID

from jose import JWTError, jwt
from litestar import status_codes
from litestar.exceptions import HTTPException

from src.user_service.config import settings
from src.user_service.infrastructure.read_models.user import UserRead


@dataclass
class AccessToken:
    token_type: Literal["access"]
    sub: str
    exp: datetime
    iat: datetime
    roles: list[str]
    permissions: list[str]


@dataclass
class RefreshToken:
    token_type: Literal["refresh"]
    sub: str
    exp: datetime
    iat: datetime


class JWTHandler:
    def __init__(self, secret_key: str = settings.SECRET_KEY, algorithm: str = settings.ALGORITHM):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, user: UserRead) -> str:
        payload = AccessToken(
            token_type="access",
            sub=str(user.id),
            exp=datetime.now(UTC).replace(tzinfo=None) + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS),
            iat=datetime.now(UTC).replace(tzinfo=None),
            roles=[assignment.role.name for assignment in user.role_assignments],
            permissions=[
                permission.code for assignment in user.role_assignments for permission in assignment.role.permissions
            ],
        )
        return jwt.encode(asdict(payload), self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user: UserRead) -> str:
        payload = RefreshToken(
            token_type="refresh",
            sub=str(user.id),
            exp=datetime.now(UTC).replace(tzinfo=None) + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS),
            iat=datetime.now(UTC).replace(tzinfo=None),
        )
        return jwt.encode(asdict(payload), self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> AccessToken | RefreshToken:
        exc = HTTPException(
            status_code=status_codes.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("token_type") == "access":
                return AccessToken(**payload)
            elif payload.get("token_type") == "refresh":
                return RefreshToken(**payload)
            else:
                raise exc
        except (JWTError, TypeError):
            raise exc


jwt_handler = JWTHandler()
