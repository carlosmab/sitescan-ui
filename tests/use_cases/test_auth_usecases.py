from uuid import uuid4
import pytest

from app.core.entities.user import User
from app.core.use_cases.auth import get_user_by_credentials, register_user
from app.utils.hashing import hash_password, verify_password



@pytest.fixture
def mock_user():
    return User(
        id=uuid4(),
        email="email@test.com",
    )


@pytest.mark.asyncio
async def test_register_user(mocker, mock_user):

    mock_repo = mocker.patch("app.core.use_cases.auth.insert_user")
    mock_repo.return_value = mock_user

    user = User(email=mock_user.email, password="1234")
    new_user = await register_user(user)

    mock_repo.assert_awaited_once()
    assert new_user is not None
    assert new_user.email == mock_user.email


@pytest.mark.asyncio
async def test_register_user_with_hashed_password(mocker, mock_user):
    mock_insert = mocker.patch("app.core.use_cases.auth.insert_user")
    mock_insert.return_value = mock_user

    user_input = User(email=mock_user.email, password="1234")
    new_user = await register_user(user_input)

    mock_insert.assert_awaited_once()
    called_user = mock_insert.await_args.args[0]

    assert called_user.email == user_input.email
    assert called_user.password != "1234"
    assert verify_password("1234", called_user.password)

    assert new_user == mock_user


@pytest.mark.asyncio
async def test_check_user_credentials(mocker, mock_user):

    mock_repo = mocker.patch("app.core.use_cases.auth.fetch_user_by_email")
    mock_user.password = hash_password("1234")
    mock_repo.return_value = mock_user

    user = await get_user_by_credentials(mock_user.email, "1234")

    mock_repo.assert_awaited_once_with(mock_user.email)
    assert user


@pytest.mark.asyncio
async def test_check_user_credentials_invalid(mocker, mock_user):

    mock_repo = mocker.patch("app.core.use_cases.auth.fetch_user_by_email")
    mock_user.password = hash_password("1234")
    mock_repo.return_value = mock_user

    user = await get_user_by_credentials(mock_user.email, "12345")

    mock_repo.assert_awaited_once_with(mock_user.email)
    assert not user