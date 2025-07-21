from litestar.dto import DataclassDTO, DTOConfig
from litestar.plugins.pydantic import PydanticDTO

from src.user_service.application.dto.user import UserWithRolesDTO
from src.user_service.domain.aggregates.user import User
from src.user_service.infrastructure.read_models.user import UserRead
from src.user_service.presentation.schemas.user import (
    CreateUserRequestSchema,
    LoginRequestSchema,
    ChangePasswordRequestSchema,
)


class UserReadResponseDTO(PydanticDTO[UserRead]):
    config = DTOConfig(max_nested_depth=3)


class UserShortResponseDTO(PydanticDTO[UserRead]):
    config = DTOConfig(
        max_nested_depth=0,
    )


class UserCreateResponseDto(DataclassDTO[User]):
    config = DTOConfig(
        exclude={
            "hashed_password",
            "role_assignments",
        },
        max_nested_depth=1,
    )


class UserCreateRequestDto(DataclassDTO[CreateUserRequestSchema]): ...


class LoginRequestDto(DataclassDTO[LoginRequestSchema]): ...


class ChangePasswordRequestDTO(DataclassDTO[ChangePasswordRequestSchema]): ...
