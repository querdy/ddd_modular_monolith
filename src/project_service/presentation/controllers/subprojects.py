from dataclasses import asdict
from typing import Annotated, List
from uuid import UUID

from dishka import FromDishka
from litestar import Controller, post, get, delete, put
from litestar.datastructures import UploadFile
from litestar.dto import DTOData
from litestar.enums import RequestEncodingType
from litestar.pagination import OffsetPagination
from litestar.params import Parameter, Body
from types_aiobotocore_s3 import S3Client

from src.common.litestar_.di.filters import get_limit_offset_filters, LimitOffsetFilterRequest
from src.common.litestar_.guards.permission import PermissionGuard
from src.common.message_bus.interfaces import IMessageBus
from src.project_service.application.protocols import IProjectServiceUoW
from src.project_service.application.services.store import generate_unique_object_key
from src.project_service.application.use_cases.read.subproject import GetSubprojectUseCase, GetSubprojectsUseCase
from src.project_service.application.use_cases.write.subproject import (
    CreateSubprojectUseCase,
    DeleteSubprojectUseCase,
    UpdateSubprojectUseCase,
)
from src.project_service.domain.entities.subproject import Subproject
from src.project_service.presentation.di.filters import get_subproject_filters
from src.project_service.presentation.dto.subproject import (
    SubprojectCreateRequestDTO,
    SubprojectCreateResponseDTO,
    SubprojectShortResponseDTO,
    SubprojectUpdateRequestDTO, SubprojectResponseDTO,
)
from src.project_service.presentation.schemas.subproject import (
    SubprojectCreateRequestSchema,
    FilterSubprojectsRequestSchema,
    SubprojectUpdateRequestSchema,
)


class SubProjectsController(Controller):
    path = "/subprojects"
    tags = ["Подпроекты"]

    @post(
        path="",
        dto=SubprojectCreateRequestDTO,
        return_dto=SubprojectCreateResponseDTO,
        guards=[PermissionGuard("subprojects:write")],
        summary="Создание нового подпроекта",
    )
    async def create(
        self,
        data: DTOData[SubprojectCreateRequestSchema],
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> Subproject:
        data_instance = data.create_instance()
        use_case = CreateSubprojectUseCase(uow, mb)
        result = await use_case.execute(
            data_instance.project_id, data_instance.name, data_instance.description, data_instance.from_template
        )
        return result

    @get(
        path="",
        return_dto=SubprojectShortResponseDTO,
        dependencies={"filters": get_subproject_filters, "pagination": get_limit_offset_filters},
        guards=[PermissionGuard("subprojects:read")],
        summary="Получение подпроектов",
    )
    async def list(
        self,
        pagination: LimitOffsetFilterRequest,
        filters: FilterSubprojectsRequestSchema,
        uow: FromDishka[IProjectServiceUoW],
    ) -> OffsetPagination[Subproject]:
        use_case = GetSubprojectsUseCase(uow)
        result = await use_case.execute(limit=pagination.limit, offset=pagination.offset, **asdict(filters))
        return result

    @get(
        path="/{subproject_id: uuid}",
        return_dto=SubprojectResponseDTO,
        guards=[PermissionGuard("subprojects:read")],
        summary="Получение подпроекта по ID",
    )
    async def get(self, subproject_id: UUID, uow: FromDishka[IProjectServiceUoW]) -> Subproject:
        use_case = GetSubprojectUseCase(uow)
        result = await use_case.execute(subproject_id)
        return result

    @delete(
        path="/{subproject_id: uuid}",
        guards=[PermissionGuard("subprojects:write")],
        summary="Удаление проекта",
    )
    async def delete(
        self,
        subproject_id: UUID,
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> None:
        use_case = DeleteSubprojectUseCase(uow, mb)
        await use_case.execute(subproject_id)

    @put(
        path="/{subproject_id: uuid}",
        dto=SubprojectUpdateRequestDTO,
        guards=[PermissionGuard("subprojects:write")],
        summary="Обновление подпроекта",
    )
    async def update(
        self,
        subproject_id: UUID,
        data: DTOData[SubprojectUpdateRequestSchema],
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> Subproject:
        data_instance = data.create_instance()
        use_case = UpdateSubprojectUseCase(uow, mb)
        result = await use_case.execute(subproject_id, data_instance.name, data_instance.description)
        return result

    @post(
        path="/{subproject_id: uuid}/upload",
        summary="Загрузка файлов для подпроекта",
    )
    async def upload_subproject_files(
        self,
        subproject_id: Annotated[UUID, Parameter()],
        data: Annotated[List[UploadFile], Body(media_type=RequestEncodingType.MULTI_PART)],
        s3_client: FromDishka[S3Client],
        uow: FromDishka[IProjectServiceUoW],
    ) -> None:
        async with uow:
            project = await uow.projects.get_by_subproject(subproject_id)
            for file in data:
                content = await file.read()
                object_key = await generate_unique_object_key(
                    s3_client=s3_client,
                    bucket="files",
                    base_path=f"subprojects/{subproject_id}",
                    filename=file.filename,
                )
                await s3_client.put_object(
                    Bucket="files",
                    Key=object_key,
                    Body=content,
                    ContentType=file.content_type,
                    ContentLength=len(content),
                )
                project.add_file_to_subproject(
                    subproject_id,
                    filename=object_key.split("/")[-1],
                    content_type=file.content_type,
                    size=len(content),
                    path=object_key,
                )
            await uow.projects.update(project)