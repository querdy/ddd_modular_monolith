from typing import Sequence

from litestar.connection import ASGIConnection
from litestar.exceptions import PermissionDeniedException
from litestar.handlers import BaseRouteHandler
from loguru import logger


class PermissionGuard:
    def __init__(self, codes: str | Sequence[str]):
        if isinstance(codes, str):
            self.codes: set = {codes}
        else:
            self.codes: set = set(codes)

    async def __call__(self, connection: ASGIConnection, _: BaseRouteHandler) -> None:
        permissions = connection.auth.permissions
        if not self.has_permission(permissions):
            raise PermissionDeniedException("В доступе отказано")

    def has_permission(self, permissions: list[str]) -> bool:
        return any(code in permissions for code in self.codes)
