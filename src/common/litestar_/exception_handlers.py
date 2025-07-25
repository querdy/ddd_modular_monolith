from litestar import status_codes, MediaType, Response, Request
from loguru import logger


def log_exception(_: Request, exc: Exception) -> Response:
    logger.debug(f"{type(exc).__name__}: {exc}")
    return Response(
        media_type=MediaType.JSON,
        content={"status_code": status_codes.HTTP_400_BAD_REQUEST, "detail": str(exc)},
        status_code=status_codes.HTTP_400_BAD_REQUEST,
    )
