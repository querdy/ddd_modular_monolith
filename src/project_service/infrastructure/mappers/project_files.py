from functools import singledispatch

from src.project_service.domain.entities.file_attachment import FileAttachment
from src.project_service.domain.value_objects.filename import FileName
from src.project_service.infrastructure.db.postgres.models import ProjectFileAttachmentModel


@singledispatch
def project_file_to_orm(obj) -> ProjectFileAttachmentModel:
    raise NotImplementedError(f"No orm mapper for {type(obj)}")


@project_file_to_orm.register
def _(obj: FileAttachment) -> ProjectFileAttachmentModel:
    return ProjectFileAttachmentModel(
        id=obj.id,
        filename=obj.filename,
        content_type=obj.content_type,
        size=obj.size,
        uploaded_at=obj.uploaded_at,
        path=obj.path,
    )


@singledispatch
def project_file_to_domain(obj) -> FileAttachment:
    raise NotImplementedError(f"No domain mapper for {type(obj)}")


@project_file_to_domain.register
def _(obj: ProjectFileAttachmentModel) -> FileAttachment:
    return FileAttachment(
        id=obj.id,
        filename=FileName(obj.filename),
        content_type=obj.content_type,
        size=obj.size,
        uploaded_at=obj.uploaded_at,
        path=obj.path,
    )
