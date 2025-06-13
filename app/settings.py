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

    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/mydb"
    db_min_size: int = 5
    db_max_size: int = 20
    db_timeout: float = 10.0


def get_settings():
    return Settings()