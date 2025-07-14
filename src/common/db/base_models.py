from uuid import UUID, uuid4
from sqlalchemy import UUID as DBUUID

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class IdBase(Base):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(DBUUID(as_uuid=True), primary_key=True, nullable=False)
