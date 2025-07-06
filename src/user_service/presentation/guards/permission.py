from litestar.connection import ASGIConnection
from litestar.exceptions import PermissionDeniedException
from litestar.handlers import BaseRouteHandler
from loguru import logger

from src.user_service.infrastructure.read_models.role import RoleRead


class PermissionGuard:
    def __init__(self, code: str):
        self.code = code

    async def __call__(self, connection: ASGIConnection, _: BaseRouteHandler) -> None:
        roles = connection.auth.roles
        permissions = connection.auth.permissions
        if not self.has_permission(permissions, self.code):
            raise PermissionDeniedException("В доступе отказано")

    @staticmethod
    def has_permission(permissions: list[str], code: str) -> bool:
        if any(permission == code for permission in permissions):
            return True
        return False
