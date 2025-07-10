from litestar.dto import DataclassDTO

from src.project_service.presentation.schemas.subproject import SubprojectCreateRequestSchema


class SubprojectCreateRequestDTO(DataclassDTO[SubprojectCreateRequestSchema]): ...