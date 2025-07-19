from typing import Generic, TypeVar, Iterable
from uuid import UUID

from pydantic import BaseModel


class Event(BaseModel):
    pass


class Query(BaseModel):
    pass


class GetUserInfoQuery(Query):
    id: UUID


class GetUserInfoListQuery(Query):
    ids: list[UUID]


class GetUserInfoResponse(BaseModel):
    id: UUID
    username: str


class GetUserInfoListResponse(BaseModel):
    users: list[GetUserInfoResponse]
