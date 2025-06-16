import pytest

from quart import Quart
from quart_auth import QuartAuth
import app.web.routes.auth 
from app.core.entities.user import User
from app.web.routes.auth import auth_bp


@pytest.fixture
def mock_app():
    app = Quart(__name__, template_folder="../../app/web/templates")
    app.register_blueprint(auth_bp)
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.secret_key = "test"

    QuartAuth(app)
    return app


@pytest.fixture
def mock_client(mock_app):
    return mock_app.test_client()


@pytest.mark.asyncio
async def test_get_login_page(mock_client):
    response = await mock_client.get("/auth/login")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_success(mocker, mock_client):

    mock_get_user = mocker.patch("app.web.routes.auth.get_user_by_credentials")
    mock_get_user.return_value = User(email="test@emai.com", password="test")
    
    mock_flash = mocker.patch("app.web.routes.auth.flash")
    mock_redirect = mocker.spy(app.web.routes.auth, "redirect")  
    
    response = await mock_client.post("/auth/login", form={"email": "test@email.com", "password": "test"})

    assert response.status_code == 302

    mock_get_user.assert_awaited_once_with("test@email.com", "test")
    mock_flash.assert_awaited_once_with("Login successful!")
    mock_redirect.assert_called_once_with("/scans")    

    response_check_session = await mock_client.get("auth/check_session")
    assert response_check_session.status_code == 200


@pytest.mark.asyncio
async def test_login_failure(mocker, mock_client):
    mock_get_user = mocker.patch("app.web.routes.auth.get_user_by_credentials")
    mock_get_user.return_value = None
    
    mock_flash = mocker.patch("app.web.routes.auth.flash")
    mock_redirect = mocker.spy(app.web.routes.auth, "redirect")  
    
    response = await mock_client.post("/auth/login", form={"email": "test@email.com", "password": "test"})

    assert response.status_code == 302
    mock_flash.assert_awaited_once_with("Invalid credentials!")
    mock_redirect.assert_called_once_with("/auth/login")

    response_check_session = await mock_client.get("auth/check_session")
    assert response_check_session.status_code == 401


@pytest.mark.asyncio
async def test_logout(mocker, mock_client):
    mock_get_user = mocker.patch("app.web.routes.auth.get_user_by_credentials")
    mock_get_user.return_value = User(email="test@emai.com", password="test")
    
    mock_flash = mocker.patch("app.web.routes.auth.flash")
    mock_redirect = mocker.spy(app.web.routes.auth, "redirect")  
    
    await mock_client.post("auth/login", form={"email": "test@email.com", "password": "test"})

    response = await mock_client.get("/auth/logout")

    assert response.status_code == 302
    mock_flash.assert_any_await("Logout successful!")
    mock_redirect.assert_any_call("/auth/login")
