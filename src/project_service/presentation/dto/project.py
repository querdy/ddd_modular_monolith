from litestar.dto import DataclassDTO

from src.project_service.presentation.schemas.project import ProjectCreateSchema


class ProjectCreateRequestDTO(DataclassDTO[ProjectCreateSchema]): ...
