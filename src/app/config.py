from typing import Any, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field, PostgresDsn


class APISettings(BaseSettings):
    PUBLIC_PREFIX: str = "/api/payments"
    INTERNAL_PREFIX: str = "/api/internal"
    ADMIN_PREFIX: str = "/api/admin"
    TRUSTED_PREFIX: str = "/api/trusted"
    TEST_PREFIX: str = "/api/test"
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

class KafkaSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="KAFKA__",
        env_file=".env",
        extra="ignore",
    )

    ENABLED: bool = True
    BROKER: str
    TOPIC: str | None = None
    NAME: str
    DEBUG: bool = False
    PRODUCER_ONLY: bool = False
    PRODUCER_REQUEST_TIMEOUT: int = 60
    PRODUCER_LINGER: float = 0.5


class KafkaProducerSettings(KafkaSettings):
    class VotesSaverConfig(BaseModel):
        topic: str = "votes_saver"
        model_config = SettingsConfigDict(env_prefix="KAFKA__VOTES_SAVES", env_file=".env")

    votes_saver: VotesSaverConfig = VotesSaverConfig()


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


class CacheSettings(BaseSettings):
    TTL: int = 300


class Settings(BaseSettings):
    DB: DatabaseSettings = DatabaseSettings()
    API: APISettings = APISettings()

    KAFKA: KafkaProducerSettings


settings = Settings()
