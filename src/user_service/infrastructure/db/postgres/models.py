from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import UUID as DBUUID, func, DateTime, String, ForeignKey

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class IdBase(Base):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        DBUUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )

class UserModel(IdBase):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    role_assignments: Mapped[list["UserRoleAssignmentModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class UserRoleAssignmentModel(IdBase):
    __tablename__ = "user_role_assignments"

    user_id: Mapped[DBUUID] = mapped_column(ForeignKey("users.id"))
    role_id: Mapped[DBUUID] = mapped_column(ForeignKey("roles.id"))
    assigned_at: Mapped[datetime]
    expires_at: Mapped[datetime | None]

    user = relationship("UserModel", backref="role_assignments")
    role = relationship("RoleModel")

class PermissionModel(IdBase):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    roles: Mapped[list["RoleModel"]] = relationship(
        secondary="role_permissions", back_populates="permissions"
    )

class RolePermissionModel(Base):
    __tablename__ = "role_permissions"

    role_id = mapped_column(DBUUID, ForeignKey("roles.id")),
    permission_id = mapped_column(DBUUID, ForeignKey("permissions.id"))

class RoleModel(IdBase):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    permissions: Mapped[list["PermissionModel"]] = relationship(
        secondary="role_permissions", backref="roles"
    )