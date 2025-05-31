from app.core.entities.user import User
from app.database.database_connection import get_db
from app.sql.user import FETCH_USER_BY_CREDENTIALS, INSERT_USER


async def insert_user(user: User) -> User | None:
    db = await get_db()
    result = await db.execute(INSERT_USER, user.model_dump(exclude={"id"}))
    return User.model_validate(dict(result)) if result else None


async def fetch_user_by_credentials(email: str, password: str) -> User | None:
    db = await get_db()
    result = await db.fetch_one(FETCH_USER_BY_CREDENTIALS, {
        "email": email,
        "password": password
    })

    return User.model_validate(dict(result)) if result else None