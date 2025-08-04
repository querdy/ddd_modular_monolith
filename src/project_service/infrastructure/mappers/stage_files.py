from functools import singledispatch

from src.project_service.domain.entities.file_attachment import FileAttachment
from src.project_service.domain.value_objects.filename import FileName
from src.project_service.infrastructure.db.postgres.models import StageFileAttachmentModel


@singledispatch
def stage_file_to_orm(obj) -> StageFileAttachmentModel:
    raise NotImplementedError(f"No orm mapper for {type(obj)}")


@stage_file_to_orm.register
def _(obj: FileAttachment) -> StageFileAttachmentModel:
    return StageFileAttachmentModel(
        id=obj.id,
        filename=obj.filename,
        content_type=obj.content_type,
        size=obj.size,
        uploaded_at=obj.uploaded_at,
        path=obj.path,
    )


@singledispatch
def stage_file_to_domain(obj) -> FileAttachment:
    raise NotImplementedError(f"No domain mapper for {type(obj)}")


@stage_file_to_domain.register
def _(obj: StageFileAttachmentModel) -> FileAttachment:
    return FileAttachment(
        id=obj.id,
        filename=FileName(obj.filename),
        content_type=obj.content_type,
        size=obj.size,
        uploaded_at=obj.uploaded_at,
        path=obj.path,
    )
