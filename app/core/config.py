from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent.parent
ENV_FILE = BASE_DIR / ".env"
LOGGING_CONFIG_FILE = BASE_DIR / "logging_config.yaml"


class PostgresSettings(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool
    max_overflow: int
    pool_size: int


class BackendSettings(BaseModel):
    host: str
    port: int


class LoggingSettings(BaseModel):
    config_path: Path = LOGGING_CONFIG_FILE
    encoding: str = "utf-8"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore"
    )
    api: BackendSettings
    db: PostgresSettings
    log: LoggingSettings = LoggingSettings()

settings = Settings()