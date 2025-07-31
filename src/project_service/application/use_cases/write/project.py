from uuid import UUID

from loguru import logger

from src.common.message_bus.interfaces import IMessageBus
from src.project_service.application.events.project import ProjectCreatedEvent
from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.domain.aggregates.project import Project


class CreateProjectUseCase:
    def __init__(self, uow: IProjectServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(self, name: str, description: str) -> Project:
        async with self.uow:
            project = Project.create(name=name, description=description)
            await self.uow.projects.add(project)
        await self.mb.publish(ProjectCreatedEvent.model_validate(project))
        return project


class DeleteProjectUseCase:
    def __init__(self, uow: IProjectServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(self, project_id: UUID) -> None:
        async with self.uow:
            await self.uow.projects.delete(project_id)


class UpdateProjectUseCase:
    def __init__(self, uow: IProjectServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(self, project_id: UUID, name: str, description: str | None = None) -> Project:
        async with self.uow:
            project = await self.uow.projects.get(project_id)
            project.update(name, description)
            await self.uow.projects.update(project)
            return project


class CreateTemplateForProjectUseCase:
    def __init__(self, uow: IProjectServiceUoW, mb: IMessageBus):
        self.uow = uow
        self.mb = mb

    async def execute(self, project_id: UUID, subproject_id: UUID) -> Project:
        async with self.uow:
            project = await self.uow.projects.get(project_id)
            project.make_template_from_subproject(subproject_id)
            await self.uow.projects.update(project)
            return project
