from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, post, get
from litestar.dto import DTOData

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.application.use_cases.read.project import GetProjectUseCase, GetProjectsUseCase
from src.project_service.application.use_cases.write.project import CreateProjectUseCase
from src.project_service.domain.aggregates.project import Project
from src.project_service.presentation.dto.project import (
    ProjectCreateRequestDTO,
    ProjectCreateResponseDTO,
    ProjectsResponseDTO,
    ProjectResponseDTO,
)
from src.project_service.presentation.schemas.project import ProjectCreateSchema
from litestar.pagination import AbstractAsyncClassicPaginator, ClassicPagination, OffsetPagination
from litestar.params import Parameter


class ProjectsController(Controller):
    path = "/projects"
    tags = ["Проекты"]

    @post(path="", dto=ProjectCreateRequestDTO, return_dto=ProjectCreateResponseDTO, summary="Создание нового проекта")
    @inject
    async def create(self, data: DTOData[ProjectCreateSchema], uow: FromDishka[IProjectServiceUoW]) -> Project:
        data_instance = data.create_instance()
        use_case = CreateProjectUseCase(uow)
        result = await use_case.execute(data_instance.name, data_instance.description)
        return result

    @get(path="", return_dto=ProjectsResponseDTO, summary="Получить проекты")
    @inject
    async def get_many(
        self,
        uow: FromDishka[IProjectServiceUoW],
        limit: Annotated[int, Parameter(ge=1, le=100, default=100)],
        offset: Annotated[int, Parameter(ge=0, default=0)],
    ) -> OffsetPagination[Project]:
        use_case = GetProjectsUseCase(uow)
        result = await use_case.execute(limit, offset)
        return result

    @get(path="/{project_id: uuid}", return_dto=ProjectResponseDTO, summary="Получение проекта по ID")
    @inject
    async def get(self, project_id: UUID, uow: FromDishka[IProjectServiceUoW]) -> Project:
        use_case = GetProjectUseCase(uow)
        result = await use_case.execute(project_id)
        return result
