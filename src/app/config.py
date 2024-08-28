from typing import Any, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn


class APISettings(BaseSettings):
    PUBLIC_PREFIX: str = "/api/payments"
    INTERNAL_PREFIX: str = "/api/payments/internal"
    ADMIN_PREFIX: str = "/api/payments/admin"
    TRUSTED_PREFIX: str = "/api/payments/trusted"
    TEST_PREFIX: str = "/api/payments/test"
    DOCS_ENABLED: bool = True
    DOCS_VERSION: str = Field("unknown", validation_alias="VERSION")
    TEST_ENABLED: bool = False

    model_config = SettingsConfigDict(
        env_prefix="API__", env_file=".env", extra="ignore"
    )


class DatabaseSettings(BaseSettings):
    APP_NAME: str
    URL: PostgresDsn
    POOL_SIZE: int = 10

    CONNECTION_TIMEOUT: int = 15
    COMMAND_TIMEOUT: int = 5

    SERVER_SETTINGS: dict[str, Any] = {}
    CONNECT_ARGS: dict[str, Any] = {}


class UvicornSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="uvicorn_",
        env_file=".env",
        extra="ignore",
    )

    app: str = "app.main:app"
    host: str = "0.0.0.0"  # nosec
    port: int = 5000
    log_level: str = "info"
    reload: bool = True
    limit_max_requests: Optional[int] = None


class Settings(BaseSettings):
    DB: DatabaseSettings = DatabaseSettings(APP_NAME="VoteApp")
    API: APISettings = APISettings()


settings = Settings()
