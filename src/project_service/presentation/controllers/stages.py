from dataclasses import asdict
from datetime import datetime
from typing import Annotated, List
from uuid import UUID

from dishka import FromDishka
from litestar import Controller, post, get, patch, delete, Request, put
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
from src.project_service.application.use_cases.read.stage import (
    GetStageUseCase,
    GetStagesUseCase,
    GetStageStatusHistoryUseCase,
)
from src.project_service.application.use_cases.write.stage import (
    CreateStageUseCase,
    UpdateStageUseCase,
    DeleteStageUseCase,
    ChangeStageStatusUseCase,
    AddMessageToStageUseCase,
)
from src.project_service.domain.entities.stage import Stage
from src.project_service.domain.entities.stage_status_history import StageStatusHistory
from src.project_service.domain.value_objects.enums import StageStatus
from src.project_service.infrastructure.read_models.stage import StageRead
from src.project_service.presentation.di.filters import get_stage_filters
from src.project_service.presentation.dto.stage import (
    StageCreateRequestDTO,
    StageCreateResponseDTO,
    StageShortResponseDTO,
    StageUpdateRequestDTO,
    ChangeStageStatusRequestDTO,
    StageReadResponseDTO,
    AddMessageToStageRequestDTO,
)
from src.project_service.presentation.schemas.stage import (
    StageCreateRequestSchema,
    FilterStageRequestSchema,
    StageUpdateRequestSchema,
    ChangeStageStatusRequestSchema,
    AddMessageToStageRequestSchema,
)


class StagesController(Controller):
    path = "/stages"
    tags = ["Этапы"]

    @post(
        path="",
        dto=StageCreateRequestDTO,
        return_dto=StageCreateResponseDTO,
        guards=[PermissionGuard("stages:write")],
        summary="Добавление этапа к подпроекту",
    )
    async def create(
        self,
        data: DTOData[StageCreateRequestSchema],
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> Stage:
        data_instance = data.create_instance()
        use_case = CreateStageUseCase(uow, mb)
        result = await use_case.execute(data_instance.subproject_id, data_instance.name, data_instance.description)
        return result

    @get(
        path="",
        return_dto=StageReadResponseDTO,
        dependencies={"filters": get_stage_filters, "pagination": get_limit_offset_filters},
        guards=[PermissionGuard("stages:read")],
        summary="Получение этапов",
    )
    async def list(
        self,
        pagination: LimitOffsetFilterRequest,
        filters: FilterStageRequestSchema,
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> OffsetPagination[StageRead]:
        use_case = GetStagesUseCase(uow, mb)
        result = await use_case.execute(limit=pagination.limit, offset=pagination.offset, **asdict(filters))
        return result

    @get(
        path="/{stage_id: uuid}/status-history",
        dependencies={"pagination": get_limit_offset_filters},
        summary="Получение истории статусов этапа",
    )
    async def stage_status_history(
        self,
        stage_id: UUID,
        pagination: LimitOffsetFilterRequest,
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> OffsetPagination[StageStatusHistory]:
        use_case = GetStageStatusHistoryUseCase(uow, mb)
        result = await use_case.execute(stage_id, pagination.limit, pagination.offset)
        return result

    @get(
        path="/{stage_id: uuid}",
        return_dto=StageReadResponseDTO,
        guards=[PermissionGuard("stages:read")],
        summary="Получение этапа по ID",
    )
    async def get(
        self,
        stage_id: UUID,
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> StageRead:
        use_case = GetStageUseCase(uow, mb)
        result = await use_case.execute(stage_id)
        return result

    @put(
        path="/{stage_id: uuid}",
        dto=StageUpdateRequestDTO,
        return_dto=StageShortResponseDTO,
        guards=[PermissionGuard("stages:write")],
        summary="Изменение этапа",
        description=f"Статусы: {', '.join(f'"{s.value}"' for s in StageStatus)}",
    )
    async def update(
        self,
        stage_id: UUID,
        data: DTOData[StageUpdateRequestSchema],
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> Stage:
        data_instance = data.create_instance()
        use_case = UpdateStageUseCase(uow, mb)
        result = await use_case.execute(stage_id, data_instance.name, data_instance.description)
        return result

    @delete(
        path="/{stage_id: uuid}",
        guards=[PermissionGuard("stages:write")],
        summary="Удаление этапа",
    )
    async def delete(
        self,
        stage_id: UUID,
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> None:
        use_case = DeleteStageUseCase(uow, mb)
        await use_case.execute(stage_id)

    @patch(
        path="/{stage_id: uuid}/status",
        dto=ChangeStageStatusRequestDTO,
        return_dto=StageReadResponseDTO,
        guards=[
            PermissionGuard(
                [
                    "stages:change_status_to_completed",
                    "stages:change_status_to_confirmed",
                ]
            )
        ],
        summary="Обновление статуса этапа",
    )
    async def change_status(
        self,
        request: Request,
        stage_id: UUID,
        data: DTOData[ChangeStageStatusRequestSchema],
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> StageRead:
        data_instance = data.create_instance()
        use_case = ChangeStageStatusUseCase(uow, mb)
        result = await use_case.execute(
            stage_id, data_instance.status, UUID(request.auth.sub), request.auth.permissions, data_instance.message
        )
        return result

    @post(
        path="/{stage_id: uuid}/message",
        dto=AddMessageToStageRequestDTO,
        summary="Добавить сообщение к этапу",
    )
    async def add_message(
        self,
        request: Request,
        stage_id: UUID,
        data: DTOData[AddMessageToStageRequestSchema],
        uow: FromDishka[IProjectServiceUoW],
        mb: FromDishka[IMessageBus],
    ) -> StageRead:
        data_instance = data.create_instance()
        use_case = AddMessageToStageUseCase(uow, mb)
        result = await use_case.execute(stage_id, UUID(request.auth.sub), data_instance.message)
        return result

    @post(
        path="/{stage_id: uuid}/upload",
        summary="Загрузка файлов для этапа",
    )
    async def upload_stage_files(
        self,
        stage_id: Annotated[UUID, Parameter()],
        data: Annotated[List[UploadFile], Body(media_type=RequestEncodingType.MULTI_PART)],
        s3_client: FromDishka[S3Client],
        uow: FromDishka[IProjectServiceUoW],
    ) -> None:
        async with uow:
            project = await uow.projects.get_by_stage(stage_id)
            for file in data:
                content = await file.read()
                object_key = await generate_unique_object_key(
                    s3_client=s3_client,
                    bucket="files",
                    base_path=f"stages/{stage_id}",
                    filename=file.filename,
                )
                await s3_client.put_object(
                    Bucket="files",
                    Key=object_key,
                    Body=content,
                    ContentType=file.content_type,
                    ContentLength=len(content),
                )
                project.add_file_to_stage(
                    stage_id,
                    filename=object_key.split("/")[-1],
                    content_type=file.content_type,
                    size=len(content),
                    path=object_key,
                )
            await uow.projects.update(project)