import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import asyncio
from logging.config import fileConfig

from alembic import context
from app.config import AlembicSettings, settings
from app.infra.db.connection import long_operation_db
from app.infra.db.models import metadata

alembic_settings = AlembicSettings()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)  # type: ignore

target_metadata = metadata

config.set_main_option("sqlalchemy.url", str(settings.DB.URL))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    async with (
        long_operation_db.engine.connect() as connection,
        asyncio.timeout(alembic_settings.MIGRATION_TIMEOUT),
    ):
        await connection.run_sync(do_run_migrations)

    await long_operation_db.engine.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = config.attributes.get("connection")

    if connectable is None:
        asyncio.run(run_async_migrations())
    else:
        do_run_migrations(connectable)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
