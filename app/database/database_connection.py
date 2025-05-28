from databases import Database
from async_lru import alru_cache
from app.settings import settings


def create_db_connection() -> Database:
    return Database(
        settings.database_url,
        min_size=settings.db_min_size,
        max_size=settings.db_max_size,
        timeout=settings.db_timeout,
    )


@alru_cache()
async def get_db() -> Database:
    db = create_db_connection()
    await db.connect()
    return db