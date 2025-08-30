from typing import Any

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    PUBLIC_PREFIX: str = "/api/vote_app"
    INTERNAL_PREFIX: str = "/api/internal"
    ADMIN_PREFIX: str = "/api/admin"
    TRUSTED_PREFIX: str = "/api/trusted"
    TEST_PREFIX: str = "/api/test"
    DOCS_ENABLED: bool = True
    DOCS_VERSION: str = Field("unknown", validation_alias="VERSION")
    TEST_ENABLED: bool = False

    model_config = SettingsConfigDict(env_prefix="API__", env_file=".env", extra="ignore")


class DatabaseSettings(BaseSettings):
    APP_NAME: str
    URL: PostgresDsn
    POOL_SIZE: int = 10

    CONNECTION_TIMEOUT: int = 15
    COMMAND_TIMEOUT: int = 5

    SERVER_SETTINGS: dict[str, Any] = {}
    CONNECT_ARGS: dict[str, Any] = {}

    model_config = SettingsConfigDict(
        env_prefix="DB__",
        env_file=".env",
        extra="ignore",
    )


class AlembicSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ALEMBIC__",
        env_file=".env",
        extra="ignore",
    )

    MIGRATION_TIMEOUT: int | float | None = 30


class UvicornSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="uvicorn_",
        env_file=".env",
        extra="ignore",
    )

    app: str = "app.main:app"
    host: str = "0.0.0.0"  # nosec  # noqa: S104
    port: int = 8200
    log_level: str = "info"
    reload: bool = True
    limit_max_requests: int | None = None


class CacheSettings(BaseSettings):
    TTL: int = 300


class Settings(BaseSettings):
    DB: DatabaseSettings = DatabaseSettings()
    API: APISettings = APISettings()

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__", extra="ignore")


settings = Settings()
