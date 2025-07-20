from litestar.dto import DataclassDTO, DTOConfig
from litestar.plugins.pydantic import PydanticDTO

from src.project_service.domain.entities.stage import Stage
from src.project_service.infrastructure.read_models.stage import StageRead
from src.project_service.presentation.schemas.stage import (
    StageCreateRequestSchema,
    StageUpdateRequestSchema,
    ChangeStageStatusRequestSchema,
    AddMessageToStageRequestSchema,
)


class StageCreateRequestDTO(DataclassDTO[StageCreateRequestSchema]): ...


class StageCreateResponseDTO(DataclassDTO[Stage]):
    config = DTOConfig(max_nested_depth=0)


class StageShortResponseDTO(DataclassDTO[Stage]):
    config = DTOConfig(max_nested_depth=0)


class StageResponseDTO(DataclassDTO[Stage]):
    config = DTOConfig(max_nested_depth=1)


class StageUpdateRequestDTO(DataclassDTO[StageUpdateRequestSchema]):
    config = DTOConfig(partial=True)


class ChangeStageStatusRequestDTO(DataclassDTO[ChangeStageStatusRequestSchema]):
    config = DTOConfig(partial=True)


class AddMessageToStageRequestDTO(DataclassDTO[AddMessageToStageRequestSchema]): ...


class StageReadResponseDTO(PydanticDTO[StageRead]): ...
