from app.core.entities.user import User
from app.repositories.user import insert_user, fetch_user_by_email
from app.utils.hashing import hash_password, verify_password


async def register_user(user: User) -> User | None:
    user.password = hash_password(user.password)
    return await insert_user(user)


async def get_user_by_credentials(email: str, password: str) -> User | None:
    user = await fetch_user_by_email(email)

    if not user:
        return None
    
    if not verify_password(password, user.password):
        return None
    
    return user
