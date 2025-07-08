from uuid import UUID

from pydantic import BaseModel


class GetInfoQuery(BaseModel):
    user_id: str


class GetInfoResponse(BaseModel):
    id: str
    name: str
