from pydantic import BaseModel

from src.common.message_bus.schemas import Query


class GetInfoQuery(Query):
    id: str


class GetInfoResponse(BaseModel):
    id: str
    name: str
