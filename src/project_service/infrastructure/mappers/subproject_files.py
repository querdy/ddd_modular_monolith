from functools import singledispatch

from src.project_service.domain.entities.file_attachment import FileAttachment
from src.project_service.domain.value_objects.filename import FileName
from src.project_service.infrastructure.db.postgres.models import SubprojectFileAttachmentModel


@singledispatch
def subproject_file_to_orm(obj) -> SubprojectFileAttachmentModel:
    raise NotImplementedError(f"No orm mapper for {type(obj)}")


@subproject_file_to_orm.register
def _(obj: FileAttachment) -> SubprojectFileAttachmentModel:
    return SubprojectFileAttachmentModel(
        id=obj.id,
        filename=obj.filename,
        content_type=obj.content_type,
        size=obj.size,
        uploaded_at=obj.uploaded_at,
        path=obj.path,
    )


@singledispatch
def subproject_file_to_domain(obj) -> FileAttachment:
    raise NotImplementedError(f"No domain mapper for {type(obj)}")


@subproject_file_to_domain.register
def _(obj: SubprojectFileAttachmentModel) -> FileAttachment:
    return FileAttachment(
        id=obj.id,
        filename=FileName(obj.filename),
        content_type=obj.content_type,
        size=obj.size,
        uploaded_at=obj.uploaded_at,
        path=obj.path,
    )
