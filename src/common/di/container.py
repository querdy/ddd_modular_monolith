from dishka import make_async_container
from dishka.integrations.litestar import LitestarProvider

from src.user_service.di.uow import UoWUserServiceProvider

container = make_async_container(
    LitestarProvider(),
    UoWUserServiceProvider(),
)
