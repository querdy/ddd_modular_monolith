from litestar.dto import DataclassDTO, DTOConfig

from src.project_service.domain.entities.subproject import Subproject
from src.project_service.presentation.schemas.subproject import SubprojectCreateRequestSchema


class SubprojectCreateRequestDTO(DataclassDTO[SubprojectCreateRequestSchema]): ...


class SubprojectCreateResponseDTO(DataclassDTO[Subproject]):
    config = DTOConfig(max_nested_depth=0)


class SubprojectResponseDTO(DataclassDTO[Subproject]):
    config = DTOConfig(max_nested_depth=1)
