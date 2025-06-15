from sqlalchemy.ext.asyncio import AsyncSession


class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
