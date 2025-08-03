from uuid import UUID

from litestar import Response, status_codes

from src.common.exceptions.application import ApplicationError
from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.config import settings
from src.user_service.domain.aggregates.blacklist import BlacklistedToken
from src.user_service.domain.aggregates.user import User
from src.user_service.infrastructure.read_models.user import UserRead
from src.user_service.presentation.schemas.user import TokenResponseSchema
from src.user_service.presentation.services.jwt import jwt_handler, RefreshToken


def generate_token_response(user: UserRead) -> Response[TokenResponseSchema]:
    access_token = jwt_handler.create_access_token(
        user=user,
    )
    refresh_token = jwt_handler.create_refresh_token(
        user=user,
    )
    response = Response(
        content=TokenResponseSchema(
            access_token=access_token,
            token_type="bearer",
        ),
        status_code=status_codes.HTTP_200_OK,
    )
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        httponly=True,
        secure=True,
        # max_age=30 * 24 * 60 * 60,  # 30 дней
        max_age=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
    )
    return response


class LoginUserUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def execute(self, email: str, password: str) -> Response:
        async with self.uow:
            user = await self.uow.users.get_by_email(email)
            if user is None or not user.hashed_password.verify(password):
                raise ApplicationError("Неверный email или пароль")
            user = await self.uow.users_read.get_by_email(email)
            return generate_token_response(user)


class UpdateAccessAndRefreshTokensUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def execute(self, user_id: UUID, refresh_token: str) -> Response:
        async with self.uow:
            if await self.uow.blacklist.exists(refresh_token):
                raise ApplicationError("Некорректный refresh токен")
            user = await self.uow.users_read.get(user_id)
            if user is None:
                raise ApplicationError("Некорректный refresh токен")
        return generate_token_response(user)


class LogoutUserUseCase:
    def __init__(self, uow: IUserServiceUoW):
        self.uow = uow

    async def execute(self, token: str, decoded_token: RefreshToken) -> Response:
        async with self.uow:
            blacklisted_token = BlacklistedToken.create(token=token, expires_at=decoded_token.exp)
            await self.uow.blacklist.add(blacklisted_token)
            response = Response(
                content="",
                status_code=status_codes.HTTP_200_OK,
            )
            response.delete_cookie("refresh_token")
            return response
