from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, post
from litestar.dto import DTOData

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.application.use_cases.write.subproject import CreateSubprojectUseCase
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.presentation.dto.subproject import SubprojectCreateRequestDTO
from src.project_service.presentation.schemas.subproject import SubprojectCreateRequestSchema


class SubProjectsController(Controller):
    path = "/subprojects"
    tags = ["Подпроекты"]

    @post(path="", dto=SubprojectCreateRequestDTO, summary="Создание нового подпроекта")
    @inject
    async def create(
        self,
        data: DTOData[SubprojectCreateRequestSchema],
        uow: FromDishka[IProjectServiceUoW],
    ) -> Subproject:
        data_instance = data.create_instance()
        use_case = CreateSubprojectUseCase(uow)
        result = await use_case.execute(data_instance.project_id, data_instance.name, data_instance.description)
        return result
