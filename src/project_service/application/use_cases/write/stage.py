from uuid import UUID

from dishka import FromDishka
from loguru import logger

from src.project_service.application.protocols import IProjectServiceUoW
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
