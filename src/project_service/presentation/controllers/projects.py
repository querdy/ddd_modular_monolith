from uuid import UUID

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, post, get
from litestar.dto import DTOData

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.application.use_cases.read.project import GetProjectUseCase
from src.project_service.application.use_cases.write.project import CreateProjectUseCase
from src.project_service.domain.aggregates.project import Project
from src.project_service.presentation.dto.project import ProjectCreateRequestDTO
from src.project_service.presentation.schemas.project import ProjectCreateSchema


class ProjectsController(Controller):
    path = "/projects"
    tags = ["Проекты"]

    @post(path="", dto=ProjectCreateRequestDTO, summary="Создание нового проекта")
    @inject
    async def create(self, data: DTOData[ProjectCreateSchema], uow: FromDishka[IProjectServiceUoW]) -> Project:
        data_instance = data.create_instance()
        use_case = CreateProjectUseCase(uow)
        result = await use_case.execute(data_instance.name, data_instance.description)
        return result

    @get(path="/{project_id: uuid}", summary="Получение проекта по ID")
    @inject
    async def get(self, project_id: UUID, uow: FromDishka[IProjectServiceUoW]) -> Project:
        use_case = GetProjectUseCase(uow)
        result = await use_case.execute(project_id)
        return result
