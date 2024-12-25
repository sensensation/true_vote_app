from contextlib import asynccontextmanager
from typing import AsyncGenerator

import orjson
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.config import DatabaseSettings, settings
from app.infra.db.utils import orjson_dumper


class AlchemyDatabase:
    def __init__(self, settings: DatabaseSettings) -> None:
        self._engine: AsyncEngine = create_async_engine(
            url=str(settings.URL),
            pool_size=settings.POOL_SIZE,
            max_overflow=0,
            pool_pre_ping=True,
            connect_args={
                "timeout": settings.CONNECTION_TIMEOUT,
                "command_timeout": settings.COMMAND_TIMEOUT,
                **settings.CONNECT_ARGS,
                "server_settings": {
                    # disable extra statement "WITH RECURSIVE typeinfo_tree ..." see
                    # https://github.com/MagicStack/asyncpg/issues/530
                    "jit": "off",
                    **settings.SERVER_SETTINGS,
                    "application_name": settings.APP_NAME,
                    "timezone": "utc",
                },
            },
            json_serializer=orjson_dumper,
            json_deserializer=orjson.loads,
        )
        self._session_factory = async_sessionmaker(bind=self._engine, expire_on_commit=False)

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory

    @asynccontextmanager
    async def session_scope(self) -> AsyncGenerator[AsyncSession, None]:
        """Provide a transactional scope around a series of operations."""

        session = self._session_factory()

        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


db = AlchemyDatabase(settings.DB)

long_operation_db = AlchemyDatabase(settings.DB.model_copy(update={"CONNECTION_TIMEOUT": 600, "COMMAND_TIMEOUT": 600}))
