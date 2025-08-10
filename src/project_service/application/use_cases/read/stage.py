from uuid import UUID

from litestar.pagination import OffsetPagination

from src.common.message_bus.interfaces import IMessageBus
from src.common.message_bus.schemas import GetUserInfoResponse, GetUserInfoListResponse, GetUserInfoListQuery
from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.entities.stage import Stage
from src.project_service.domain.entities.stage_status_history import StageStatusHistory
from src.project_service.infrastructure.read_models.file_attachment import FileAttachmentRead
from src.project_service.infrastructure.read_models.message import MessageRead
from src.project_service.infrastructure.read_models.stage import StageRead
from src.project_service.presentation.pagination import StageOffsetPagination, StageStatusHistoryOffsetPagination


class GetStageUseCase:
    def __init__(self, uow: IProjectServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(self, stage_id: UUID) -> StageRead:
        async with self.uow:
            stage: Stage = await self.uow.projects_read.get_stage(stage_id)
            author_ids = [message.author_id for message in stage.messages]
            user_map: dict[UUID, GetUserInfoResponse] = {}
            query_result = await self.mb.query(
                GetUserInfoListQuery(ids=list(author_ids)), response_model=GetUserInfoListResponse
            )
            for user in query_result.users:
                user_map[user.id] = user
            return StageRead(
                id=stage.id,
                name=stage.name,
                description=stage.description,
                created_at=stage.created_at,
                updated_at=stage.updated_at,
                status=stage.status,
                messages=[
                    MessageRead(
                        id=msg.id,
                        created_at=msg.created_at,
                        text=msg.text,
                        author=user_map.get(msg.author_id, None).model_dump(),
                    )
                    for msg in stage.messages
                ],
                files=[FileAttachmentRead(
                    id=file.id,
                    filename=file.filename,
                    content_type=file.content_type,
                    size=file.size,
                    uploaded_at=file.uploaded_at,
                    path=file.path,
                ) for file in stage.files],
            )


class GetStagesUseCase:
    def __init__(self, uow: IProjectServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(self, limit: int, offset: int, **filters) -> OffsetPagination[StageRead]:
        async with self.uow:
            return await StageOffsetPagination(self.uow, self.mb)(limit, offset, **filters)


class GetStageStatusHistoryUseCase:
    def __init__(self, uow: IProjectServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(self, stage_id: UUID, limit: int, offset: int) -> OffsetPagination[StageStatusHistory]:
        async with self.uow:
            return await StageStatusHistoryOffsetPagination(self.uow, self.mb)(
                limit,
                offset,
                filters={"stage_id": stage_id},
            )
