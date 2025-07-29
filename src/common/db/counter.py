import functools

from loguru import logger
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession
import contextlib


def count_queries(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        session: AsyncSession = getattr(self, "session", None)
        if not isinstance(session, AsyncSession):
            raise ValueError("Экземпляр класса должен иметь self.session типа AsyncSession")

        counter = {"count": 0}

        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            counter["count"] += 1

        conn = await session.connection()
        event.listen(conn.sync_connection, "before_cursor_execute", before_cursor_execute)

        try:
            result = await func(self, *args, **kwargs)
            logger.warning(f"[{self.__class__.__name__}.{func.__name__}] SQL-запросов выполнено: {counter['count']}")
            return result
        finally:
            event.remove(conn.sync_connection, "before_cursor_execute", before_cursor_execute)

    return wrapper
