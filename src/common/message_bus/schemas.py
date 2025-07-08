from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Event(BaseModel):
    pass


class Query(BaseModel, Generic[T]):
    pass
