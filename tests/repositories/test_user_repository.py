from unittest.mock import AsyncMock
from uuid import uuid4
import pytest

from app.core.entities.user import User
from app.repositories.user import fetch_user_by_email, insert_user


@pytest.fixture
def mock_db():
    return AsyncMock()


@pytest.fixture
def mock_user():
    return User(
        id=uuid4(),
        email="email@test.com",
        password="thisisapassword"
    )


@pytest.mark.asyncio
async def test_insert_user(mocker, mock_db, mock_user):

    mock_db.execute.return_value = {
        "id": str(uuid4()),
        "email": mock_user.email,
        "password": mock_user.password,
    }

    mocker.patch("app.repositories.user.get_db", return_value = mock_db)

    new_user = await insert_user(mock_user)

    mock_db.execute.assert_awaited_once()
    assert isinstance(new_user, User)
    assert new_user is not None


@pytest.mark.asyncio
async def test_fetch_user_by_email(mocker, mock_db, mock_user):
    
    mock_db.fetch_one.return_value = {
        "id": str(uuid4()),
        "email": mock_user.email,
    }

    mocker.patch("app.repositories.user.get_db", return_value = mock_db)

    user = await fetch_user_by_email(mock_user.email)

    mock_db.fetch_one.assert_awaited_once()
    assert isinstance(user, User)
    assert user.email == mock_user.email