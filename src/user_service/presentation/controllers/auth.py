from typing import Annotated

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, post, Response, get, Request, status_codes
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body
from loguru import logger

from src.common.exceptions.application import ApplicationError
from src.common.exceptions.infrastructure import InfrastructureError
from src.user_service.application.protocols import IUserServiceUoW
from src.user_service.application.use_cases.auth import (
    LoginUserUseCase,
    UpdateAccessAndRefreshTokensUseCase,
    LogoutUserUseCase,
)
from src.user_service.presentation.schemas.user import (
    LoginRequestSchema,
    TokenResponseSchema,
)
from src.user_service.presentation.dto.user import LoginRequestDto


class AuthController(Controller):
    path = "/auth"
    tags = ["Авторизация"]

    @post("/login", dto=LoginRequestDto, exclude_from_auth=True, summary="Авторизация")
    async def login(
        self,
        uow: FromDishka[IUserServiceUoW],
        data: Annotated[LoginRequestSchema, Body(media_type=RequestEncodingType.URL_ENCODED)],
    ) -> Response[TokenResponseSchema]:
        use_case = LoginUserUseCase(uow)
        response = await use_case.execute(email=data.email, password=data.password)
        return response

    @get("/refresh", summary="Обновление access и refresh токенов")
    async def refresh_access_token(
        self, request: Request, uow: FromDishka[IUserServiceUoW]
    ) -> Response[TokenResponseSchema]:
        user_case = UpdateAccessAndRefreshTokensUseCase(uow)
        result = await user_case.execute(request.auth.sub, refresh_token=request.user)
        return result

    @get("/logout", summary="Выход (удаление refresh token)")
    async def logout(self, request: Request, uow: FromDishka[IUserServiceUoW]) -> Response:
        use_case = LogoutUserUseCase(uow)
        result = await use_case.execute(request.user, request.auth)
        return result
