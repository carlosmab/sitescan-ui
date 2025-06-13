from databases import Database
from functools import lru_cache
from app.settings import get_settings


def create_db_object() -> Database:
    settings = get_settings()

    return Database(
        settings.database_url,
        min_size=settings.db_min_size,
        max_size=settings.db_max_size,
        timeout=settings.db_timeout,
    )


@lru_cache()
def get_db() -> Database:
    return create_db_object()
    