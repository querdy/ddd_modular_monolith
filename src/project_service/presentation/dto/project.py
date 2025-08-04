from litestar.dto import DataclassDTO, DTOConfig
from litestar.plugins.pydantic import PydanticDTO

from src.project_service.domain.aggregates.project import Project
from src.project_service.infrastructure.read_models.project import ProjectRead
from src.project_service.presentation.schemas.project import (
    ProjectCreateSchema,
    ProjectUpdateRequestSchema,
    CreateTemplateRequestSchema,
)


class ProjectCreateRequestDTO(DataclassDTO[ProjectCreateSchema]): ...


class ProjectCreateResponseDTO(DataclassDTO[Project]):
    config = DTOConfig(max_nested_depth=0)


class ProjectShortResponseDTO(DataclassDTO[Project]):
    config = DTOConfig(
        max_nested_depth=0,
        exclude={
            "subprojects",
            "template",
        },
    )


class ProjectReadResponseDTO(PydanticDTO[ProjectRead]):
    config = DTOConfig(
        max_nested_depth=3,
    )


class ProjectReadShortResponseDTO(PydanticDTO[ProjectRead]):
    config = DTOConfig(
        max_nested_depth=0,
    )


class ProjectResponseDTO(DataclassDTO[Project]):
    config = DTOConfig(
        max_nested_depth=2,
        exclude={"subprojects"},
    )


class ProjectUpdateRequestDTO(DataclassDTO[ProjectUpdateRequestSchema]):
    config = DTOConfig(partial=True)


class CreateTemplateRequestDTO(DataclassDTO[CreateTemplateRequestSchema]): ...
