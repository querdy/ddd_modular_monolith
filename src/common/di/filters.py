from dataclasses import dataclass
from typing import Annotated

from litestar.params import Parameter


@dataclass
class LimitOffsetFilterRequest:
    limit: int
    offset: int


async def get_limit_offset_filters(
    limit: Annotated[int, Parameter(ge=1, le=100, default=100)],
    offset: Annotated[int, Parameter(ge=0, default=0)],
) -> LimitOffsetFilterRequest:
    return LimitOffsetFilterRequest(limit, offset)
