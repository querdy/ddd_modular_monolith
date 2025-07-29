from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.counter import count_queries
from src.project_service.domain.entities.stage_status_history import StageStatusHistory
from src.project_service.infrastructure.db.postgres.models import StageStatusHistoryModel
from src.project_service.infrastructure.mappers.stage_status_history import (
    stage_status_history_to_orm,
    stage_status_history_to_domain,
)


class StageStatusHistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, obj: StageStatusHistory) -> None:
        orm_obj = stage_status_history_to_orm(obj)
        self.session.add(orm_obj)

    @count_queries
    async def count(self, **filters) -> int:
        stmt = select(func.count()).select_from(StageStatusHistoryModel)
        if stage_id := filters.get("stage_id", False):
            stmt = stmt.where(StageStatusHistoryModel.stage_id == stage_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    @count_queries
    async def get_many(self, limit: int, offset: int, **filters) -> list[StageStatusHistory]:
        stmt = (
            select(StageStatusHistoryModel)
            .order_by(desc(StageStatusHistoryModel.changed_at))
            .limit(limit)
            .offset(offset)
        )
        if stage_id := filters.get("stage_id", False):
            stmt = stmt.where(StageStatusHistoryModel.stage_id == stage_id)
        result = await self.session.execute(stmt)
        orn_objs = result.unique().scalars().all()
        return [stage_status_history_to_domain(orn_obj) for orn_obj in orn_objs]
