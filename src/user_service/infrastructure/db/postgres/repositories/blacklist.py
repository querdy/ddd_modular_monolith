from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.user_service.domain.aggregates.blacklist import BlacklistedToken
from src.user_service.infrastructure.db.postgres.models import BlacklistedTokenModel
from src.user_service.infrastructure.mappers.blacklist import blacklisted_token_to_orm


class BlacklistRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, blacklisted_token: BlacklistedToken) -> None:
        blacklisted_token_orm = blacklisted_token_to_orm(blacklisted_token)
        self.session.add(blacklisted_token_orm)

    async def exists(self, blacklisted_token: str) -> bool:
        stmt = select(1).where(BlacklistedTokenModel.token == blacklisted_token).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar() is not None
