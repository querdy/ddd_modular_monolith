from litestar.dto import DataclassDTO

from src.user_service.presentation.schemas.user import TokenResponseSchema


class TokenResponseDTO(DataclassDTO[TokenResponseSchema]): ...
