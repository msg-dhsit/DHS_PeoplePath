import os
from functools import lru_cache
from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    app_name: str = "Resource Management Portal API"
    secret_key: str = os.environ.get("SECRET_KEY", "dev-secret")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    database_url: AnyUrl = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/peoplepath")
    cors_origins: str = os.environ.get("CORS_ORIGINS", "http://localhost:3000,https://localhost:3000")
    ai_provider: str = os.environ.get("AI_PROVIDER", "mock")
    azure_openai_endpoint: str = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_api_key: str = os.environ.get("AZURE_OPENAI_API_KEY", "")
    azure_openai_deployment: str = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
    scheduler_enabled: bool = True

    class Config:
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
