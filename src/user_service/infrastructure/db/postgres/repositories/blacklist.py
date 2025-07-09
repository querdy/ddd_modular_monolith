from sqlalchemy.ext.asyncio import AsyncSession


class BlacklistRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, ) -> None:
        ...
