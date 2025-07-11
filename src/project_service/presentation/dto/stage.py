from litestar.dto import DataclassDTO, DTOConfig

from src.project_service.domain.entities.stage import Stage
from src.project_service.presentation.schemas.stage import StageCreateRequestSchema


class StageCreateRequestDTO(DataclassDTO[StageCreateRequestSchema]): ...


class StageCreateResponseDTO(DataclassDTO[Stage]):
    config = DTOConfig(max_nested_depth=0)


class StageResponseDTO(DataclassDTO[Stage]):
    config = DTOConfig(max_nested_depth=1)
