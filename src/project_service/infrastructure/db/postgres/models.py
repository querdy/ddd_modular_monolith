from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import UUID as DBUUID, String, ForeignKey, DateTime, func, Float, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship


from src.common.db.base_models import IdBase


class ProjectModel(IdBase):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    template: Mapped["SubprojectTemplateModel"] = relationship(
        "SubprojectTemplateModel",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    progress: Mapped[float] = mapped_column(Float, nullable=False)
    subprojects: Mapped[list["SubprojectModel"]] = relationship(
        "SubprojectModel",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    files: Mapped[list["ProjectFileAttachmentModel"]] = relationship(
        "ProjectFileAttachmentModel",
        back_populates="project",
        cascade="all, delete-orphan",
    )


class ProjectFileAttachmentModel(IdBase):
    __tablename__ = "project_files"

    project_id: Mapped[UUID] = mapped_column(DBUUID, ForeignKey("projects.id", ondelete="CASCADE"))
    project: Mapped[ProjectModel] = relationship(back_populates="files")

    filename: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False, unique=True)


class SubprojectModel(IdBase):
    __tablename__ = "subprojects"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    progress: Mapped[float] = mapped_column(Float, nullable=False)
    project_id: Mapped[UUID] = mapped_column(DBUUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)

    files: Mapped[list["SubprojectFileAttachmentModel"]] = relationship(
        "SubprojectFileAttachmentModel",
        back_populates="subproject",
        cascade="all, delete-orphan",
    )

    project: Mapped["ProjectModel"] = relationship(
        "ProjectModel",
        back_populates="subprojects",
    )
    stages: Mapped[list["StageModel"]] = relationship(
        "StageModel",
        back_populates="subproject",
        cascade="all, delete-orphan",
    )

class SubprojectFileAttachmentModel(IdBase):
    __tablename__ = "subproject_files"

    subproject_id: Mapped[UUID] = mapped_column(DBUUID, ForeignKey("subprojects.id", ondelete="CASCADE"))
    subproject: Mapped[SubprojectModel] = relationship(back_populates="files")

    filename: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False, unique=True)

class StageModel(IdBase):
    __tablename__ = "stages"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    subproject_id: Mapped[UUID] = mapped_column(
        DBUUID,
        ForeignKey("subprojects.id", ondelete="CASCADE"),
        nullable=False,
    )

    files: Mapped[list["StageFileAttachmentModel"]] = relationship(
        "StageFileAttachmentModel",
        back_populates="stage",
        cascade="all, delete-orphan",
    )

    subproject: Mapped["SubprojectModel"] = relationship(
        "SubprojectModel",
        back_populates="stages",
    )
    messages: Mapped[list["MessageModel"]] = relationship(
        "MessageModel",
        back_populates="stage",
        cascade="all, delete-orphan",
        order_by="asc(MessageModel.created_at)",
    )

class StageFileAttachmentModel(IdBase):
    __tablename__ = "stage_files"

    stage_id: Mapped[UUID] = mapped_column(DBUUID, ForeignKey("stages.id", ondelete="CASCADE"))
    stage: Mapped[StageModel] = relationship(back_populates="files")

    filename: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False, unique=True)

class MessageModel(IdBase):
    __tablename__ = "messages"

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    author_id: Mapped[UUID] = mapped_column(DBUUID, nullable=False)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    stage_id: Mapped[UUID] = mapped_column(
        DBUUID,
        ForeignKey("stages.id", ondelete="CASCADE"),
        nullable=False,
    )

    stage: Mapped[StageModel] = relationship(
        "StageModel",
        back_populates="messages",
    )


class SubprojectTemplateModel(IdBase):
    __tablename__ = "subproject_templates"

    project_id: Mapped[UUID] = mapped_column(
        DBUUID(as_uuid=True),
        ForeignKey("projects.id"),
        # unique=True,
        nullable=False,
    )
    project = relationship(
        "ProjectModel",
        back_populates="template",
    )
    stages: Mapped[list["StageTemplateModel"]] = relationship(
        "StageTemplateModel",
        back_populates="subproject_template",
        cascade="all, delete-orphan",
    )


class StageTemplateModel(IdBase):
    __tablename__ = "stage_templates"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    subproject_template_id: Mapped[UUID] = mapped_column(
        DBUUID,
        ForeignKey("subproject_templates.id", ondelete="CASCADE"),
        # unique=True,
        nullable=False,
    )
    subproject_template: Mapped["SubprojectTemplateModel"] = relationship(
        "SubprojectTemplateModel",
        back_populates="stages",
    )


class StageStatusHistoryModel(IdBase):
    __tablename__ = "stage_status_history"

    stage_id: Mapped[UUID] = mapped_column(DBUUID(as_uuid=True))
    to_status: Mapped[str] = mapped_column(String(16), nullable=False)
    changed_by: Mapped[UUID] = mapped_column(DBUUID(as_uuid=True))
    changed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
