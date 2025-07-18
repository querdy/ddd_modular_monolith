from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel


class Event(BaseModel):
    pass


class Query(BaseModel):
    pass


class GetUserInfoQuery(Query):
    id: UUID


class GetUserInfoResponse(BaseModel):
    id: UUID
    username: str
