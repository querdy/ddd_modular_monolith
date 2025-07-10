from functools import singledispatch

from src.user_service.domain.aggregates.blacklist import BlacklistedToken
from src.user_service.infrastructure.db.postgres.models import UserModel, BlacklistedTokenModel


@singledispatch
def blacklisted_token_to_orm(obj):
    raise NotImplementedError(f"No domain mapper for {type(obj)}")


@blacklisted_token_to_orm.register
def _(obj: BlacklistedToken) -> BlacklistedTokenModel:
    return BlacklistedTokenModel(
        id=obj.id, token=obj.token, expires_at=obj.expires_at, reason=obj.reason, created_at=obj.created_at
    )
