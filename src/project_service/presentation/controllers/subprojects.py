from uuid import UUID

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, post, get
from litestar.dto import DTOData

from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.application.use_cases.read.subproject import GetSubprojectUseCase
from src.project_service.application.use_cases.write.subproject import CreateSubprojectUseCase
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.presentation.dto.subproject import (
    SubprojectCreateRequestDTO,
    SubprojectCreateResponseDTO,
    SubprojectResponseDTO,
)
from src.project_service.presentation.schemas.subproject import SubprojectCreateRequestSchema


class SubProjectsController(Controller):
    path = "/subprojects"
    tags = ["Подпроекты"]

    @post(
        path="",
        dto=SubprojectCreateRequestDTO,
        return_dto=SubprojectCreateResponseDTO,
        summary="Создание нового подпроекта",
    )
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

    @get(path="/{subproject_id: uuid}", return_dto=SubprojectResponseDTO, summary="Получение подпроекта по ID")
    @inject
    async def get(self, subproject_id: UUID, uow: FromDishka[IProjectServiceUoW]) -> Subproject:
        use_case = GetSubprojectUseCase(uow)
        result = await use_case.execute(subproject_id)
        return result
