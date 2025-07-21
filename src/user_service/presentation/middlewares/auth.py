from uuid import UUID

from jose import JWTError
from litestar import status_codes
from litestar.connection import ASGIConnection
from litestar.exceptions import HTTPException, NotAuthorizedException
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult
from loguru import logger

from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.infrastructure.read_models.user import UserRead
from src.user_service.presentation.services.jwt import jwt_handler


class AuthMiddleware(AbstractAuthenticationMiddleware):
    @staticmethod
    async def get_user_by_token_sub(token_sub: str, connection: ASGIConnection) -> UserRead | None:
        async with connection.app.state.dishka_container() as scope:
            uow: IUserServiceUoW = await scope.get(IUserServiceUoW)
            async with uow:
                user = await uow.users_read.get(UUID(token_sub))
                return user

    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:
        path = connection.scope["path"]
        if path in [
            "/schema",
            "/docs",
            "/docs/openapi.json",
            "/docs/swagger",
            "/docs/redoc",
            "/docs/stoplight",
            "/docs/rapid",
            "/docs/scalar",
            "/metrics",
        ]:
            return AuthenticationResult(user=None, auth=None)

        if path in ["/api/auth/refresh", "/api/auth/logout"]:
            token = connection.cookies.get("refresh_token")
            if token is not None and token.lower().startswith("bearer "):
                token = token.split(" ")[1]
            else:
                raise NotAuthorizedException("Отсутствует refresh токен")
            decoded_token = jwt_handler.decode_token(token)
            return AuthenticationResult(user=token, auth=decoded_token)

        auth_header = connection.headers.get("authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header.split(" ")[1]
            decoded_token = jwt_handler.decode_token(token)
            return AuthenticationResult(user=None, auth=decoded_token)
        raise NotAuthorizedException("Необходима авторизация")
