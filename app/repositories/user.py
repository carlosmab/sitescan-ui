from app.core.entities.user import User
from app.db import get_db
from app.sql.user import FETCH_USER_BY_EMAIL, INSERT_USER


async def insert_user(user: User) -> User | None:
    result = await get_db().execute(INSERT_USER, user.model_dump(exclude={"id"}))
    return User.model_validate(dict(result)) if result else None


async def fetch_user_by_email(email: str,) -> User | None:
    result = await get_db().fetch_one(FETCH_USER_BY_EMAIL, {
        "email": email,
    })

    return User.model_validate(dict(result)) if result else None