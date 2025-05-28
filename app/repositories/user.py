from app.core.entities.user import User
from app.database.database_connection import get_db
from app.sql.user import INSERT_USER


async def insert_user(user: User) -> User | None:
    db = await get_db()
    result = await db.fetch_one(INSERT_USER, user.model_dump(exclude={"id"}))
    return User.model_validate(dict(result)) if result else None