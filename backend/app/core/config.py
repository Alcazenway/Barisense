from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    app_name: str = "Barisense API"
    environment: Literal["dev", "test", "prod"] = "dev"
    api_v1_prefix: str = "/api/v1"
    allow_origins: list[str] = ["*"]
    version: str = "0.1.0"
    database_url: str = "sqlite:///./barisense.db"
    api_key_header: str = "X-API-Key"
    api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="BARISENSE_",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
