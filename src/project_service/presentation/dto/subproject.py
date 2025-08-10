from litestar.dto import DataclassDTO, DTOConfig
from litestar.plugins.pydantic import PydanticDTO

from src.project_service.domain.entities.subproject import Subproject
from src.project_service.infrastructure.read_models.subproject import SubprojectRead
from src.project_service.presentation.schemas.subproject import (
    SubprojectCreateRequestSchema,
    SubprojectUpdateRequestSchema,
)


class SubprojectCreateRequestDTO(DataclassDTO[SubprojectCreateRequestSchema]): ...


class SubprojectCreateResponseDTO(DataclassDTO[Subproject]):
    config = DTOConfig(max_nested_depth=0)


class SubprojectShortResponseDTO(DataclassDTO[Subproject]):
    config = DTOConfig(max_nested_depth=0)


class SubprojectResponseDTO(DataclassDTO[Subproject]):
    config = DTOConfig(max_nested_depth=1, exclude={"stages", })


class SubprojectReadDTO(PydanticDTO[SubprojectRead]): ...


class SubprojectUpdateRequestDTO(DataclassDTO[SubprojectUpdateRequestSchema]):
    config = DTOConfig(partial=True)
