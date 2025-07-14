from uuid import UUID

from dishka import FromDishka
from loguru import logger

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.entities.message import Message
from src.project_service.domain.entities.stage import Stage


class CreateStageUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, subproject_id: UUID, name: str, description: str):
        async with self.uow:
            project = await self.uow.projects.get_by_subproject(subproject_id)

            stage = Stage.create(name=name, description=description)
            subproject = project.get_subproject_by_id(subproject_id)
            subproject.add_stage(stage)
            await self.uow.projects.update(project)
            return stage


class UpdateStageUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, stage_id: UUID, name: str | None, description: str | None, status: str | None) -> Stage:
        async with self.uow:
            project = await self.uow.projects.get_by_stage(stage_id)
            stage = project.update_stage(stage_id, name, description, status)
            await self.uow.projects.update(project)
            return stage


class DeleteStageUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, stage_id: UUID) -> None:
        async with self.uow:
            project = await self.uow.projects.get_by_stage(stage_id)
            project.remove_stage(stage_id)
            await self.uow.projects.update(project)

class ChangeStageStatusUseCase:
    def __init__(self, uow: IProjectServiceUoW):
        self.uow = uow

    async def execute(self, stage_id: UUID, status: str, user_id: UUID, message: str | None = None) -> Stage:
        if message is not None:
            message = Message.create(user_id, message)
        project = await self.uow.projects.get_by_stage(stage_id)

