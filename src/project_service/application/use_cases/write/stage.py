from uuid import UUID

from src.common.exceptions.application import ApplicationPermissionDeniedError
from src.common.message_bus.interfaces import IMessageBus
from src.common.message_bus.schemas import (
    GetUserInfoResponse,
    GetUserInfoListQuery,
    GetUserInfoListResponse,
)
from src.project_service.application.events.stage import StageStatusChangedEvent
from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.entities.message import Message
from src.project_service.domain.entities.stage import Stage
from src.project_service.domain.value_objects.enums import StageStatus
from src.project_service.infrastructure.read_models.file_attachment import FileAttachmentRead
from src.project_service.infrastructure.read_models.message import MessageRead
from src.project_service.infrastructure.read_models.stage import StageRead


class CreateStageUseCase:
    def __init__(self, uow: IProjectServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(self, subproject_id: UUID, name: str, description: str):
        async with self.uow:
            project = await self.uow.projects.get_by_subproject(subproject_id)

            stage = Stage.create(name=name, description=description)
            subproject = project.get_subproject_by_id(subproject_id)
            subproject.add_stage(stage)
            await self.uow.projects.update(project)
            return stage


class UpdateStageUseCase:
    def __init__(self, uow: IProjectServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(self, stage_id: UUID, name: str, description: str | None) -> Stage:
        async with self.uow:
            project = await self.uow.projects.get_by_stage(stage_id)
            stage = project.update_stage(stage_id, name, description)
            await self.uow.projects.update(project)
            return stage


class DeleteStageUseCase:
    def __init__(self, uow: IProjectServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(self, stage_id: UUID) -> None:
        async with self.uow:
            project = await self.uow.projects.get_by_stage(stage_id)
            project.remove_stage(stage_id)
            await self.uow.projects.update(project)


class ChangeStageStatusUseCase:
    def __init__(self, uow: IProjectServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(
        self,
        stage_id: UUID,
        status: str,
        user_id: UUID,
        permissions: list[str],
        message: str | None = None,
    ) -> StageRead:
        async with self.uow:
            if status == StageStatus.COMPLETED and "stages:change_status_to_completed" not in permissions:
                raise ApplicationPermissionDeniedError(
                    f"У вас недостаточно прав для изменения статуса этапа на `{status}`"
                )
            if message is not None:
                message = Message.create(user_id, message)
            project = await self.uow.projects.get_by_stage(stage_id)
            new_stage = project.change_stage_status(stage_id, status, message)
            await self.uow.projects.update(project)

        await self.mb.publish(
            StageStatusChangedEvent(
                stage_id=new_stage.id,
                to_status=new_stage.status,
                changed_by=user_id,
                changed_at=new_stage.updated_at,
            )
        )
        author_ids = {msg.author_id for msg in new_stage.messages}
        user_map: dict[UUID, GetUserInfoResponse] = {}
        query_result = await self.mb.query(
            GetUserInfoListQuery(ids=list(author_ids)),
            response_model=GetUserInfoListResponse,
        )
        for user in query_result.users:
            user_map[user.id] = user
        return StageRead(
            id=new_stage.id,
            name=new_stage.name,
            description=new_stage.description,
            created_at=new_stage.created_at,
            updated_at=new_stage.updated_at,
            status=new_stage.status,
            messages=[
                MessageRead(
                    id=msg.id,
                    created_at=msg.created_at,
                    text=msg.text,
                    author=user_map[msg.author_id].model_dump(),
                )
                for msg in new_stage.messages
            ],
            files=[FileAttachmentRead(
                id=file.id,
                filename=file.filename,
                content_type=file.content_type,
                size=file.size,
                uploaded_at=file.uploaded_at,
                path=file.path,
            ) for file in new_stage.files],
        )


class AddMessageToStageUseCase:
    def __init__(self, uow: IProjectServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(self, stage_id: UUID, user_id: UUID, message: str) -> StageRead:
        async with self.uow:
            if message is not None:
                message = Message.create(user_id, message)
            project = await self.uow.projects.get_by_stage(stage_id)
            new_stage = project.add_message_to_stage(stage_id, message)
            await self.uow.projects.update(project)

            author_ids = {msg.author_id for msg in new_stage.messages}
            user_map: dict[UUID, GetUserInfoResponse] = {}
            query_result = await self.mb.query(
                GetUserInfoListQuery(ids=list(author_ids)), response_model=GetUserInfoListResponse
            )
            for user in query_result.users:
                user_map[user.id] = user
            return StageRead(
                id=new_stage.id,
                name=new_stage.name,
                description=new_stage.description,
                created_at=new_stage.created_at,
                updated_at=new_stage.updated_at,
                status=new_stage.status,
                messages=[
                    MessageRead(
                        id=msg.id,
                        created_at=msg.created_at,
                        text=msg.text,
                        author=user_map.get(msg.author_id, None).model_dump(),
                    )
                    for msg in new_stage.messages
                ],
                files=[FileAttachmentRead(
                    id=file.id,
                    filename=file.filename,
                    content_type=file.content_type,
                    size=file.size,
                    uploaded_at=file.uploaded_at,
                    path=file.path,
                ) for file in new_stage.files],
            )
