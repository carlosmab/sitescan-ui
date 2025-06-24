from databases import Database
from functools import lru_cache
from app.settings import get_settings


def create_db_object() -> Database:
    settings = get_settings()

    return Database(
        settings.DATABASE_URL,
        min_size=settings.DB_POOL_MIN_SIZE,
        max_size=settings.DB_POOL_MAX_SIZE,
        timeout=settings.DB_TIMEOUT,
    )


@lru_cache()
def get_db() -> Database:
    return create_db_object()
    