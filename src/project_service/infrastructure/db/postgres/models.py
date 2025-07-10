from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import UUID as DBUUID, String, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship


from src.common.db.base_models import IdBase


class ProjectModel(IdBase):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    subprojects: Mapped[list["SubprojectModel"]] = relationship(
        "SubprojectModel",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class SubprojectModel(IdBase):
    __tablename__ = "subprojects"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False)

    project_id: Mapped[UUID] = mapped_column(DBUUID, ForeignKey("projects.id"), nullable=False)
    project: Mapped["ProjectModel"] = relationship(
        "ProjectModel",
        back_populates="subprojects",
        lazy="selectin",
    )
    stages: Mapped[list["StageModel"]] = relationship(
        "StageModel",
        back_populates="subproject",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class StageModel(IdBase):
    __tablename__ = "stages"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False)

    subproject_id: Mapped[UUID] = mapped_column(DBUUID, ForeignKey("subprojects.id"), nullable=True)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    subproject: Mapped["SubprojectModel"] = relationship(
        "SubprojectModel",
        back_populates="stages",
        lazy="selectin",
    )
