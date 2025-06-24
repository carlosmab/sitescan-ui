from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        nested_model_default_partial_update=False,
        env_prefix="",
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=False,
        env_nested_delimiter="__",
        env_nested_max_split=1,
    )
    
    SECRET_KEY: str = "dev-secret"
    DEBUG: bool = True
    WTF_CSRF_ENABLED: bool = True

    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/mydb"
    DB_POOL_MIN_SIZE: int = 5
    DB_POOL_MAX_SIZE: int = 20
    DB_TIMEOUT: float = 10.0


@lru_cache
def get_settings():
    return Settings()