"""Configuration loaded from environment."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+asyncpg://localhost:5432/chimera"
    weaviate_url: str = "http://localhost:8080"
    weaviate_api_key: str = ""
    redis_url: str = "redis://localhost:6379/0"
    confidence_high: float = 0.90
    confidence_medium: float = 0.70


settings = Settings()
