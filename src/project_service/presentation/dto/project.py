from litestar.dto import DataclassDTO, DTOConfig

from src.project_service.domain.aggregates.project import Project
from src.project_service.presentation.schemas.project import ProjectCreateSchema, ProjectUpdateRequestSchema


class ProjectCreateRequestDTO(DataclassDTO[ProjectCreateSchema]): ...


class ProjectCreateResponseDTO(DataclassDTO[Project]):
    config = DTOConfig(max_nested_depth=0)


class ProjectShortResponseDTO(DataclassDTO[Project]):
    config = DTOConfig(max_nested_depth=0)


class ProjectResponseDTO(DataclassDTO[Project]):
    config = DTOConfig(max_nested_depth=1)


class ProjectUpdateRequestDTO(DataclassDTO[ProjectUpdateRequestSchema]):
    config = DTOConfig(partial=True)
