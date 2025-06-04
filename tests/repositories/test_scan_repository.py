from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest

from app.core.entities.scan import Scan, ScrapResult
from app.core.entities.user import User
from app.repositories.scan import fetch_scans_by_user_id, fetch_scan_by_id, insert_scan, update_scrap_result, update_analysis_result


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

@pytest.fixture
def mock_scan(mock_user):
    return Scan(
        id=uuid4(),
        url="www.test.scan",
        user_id=mock_user.id,
        created_at=datetime.now()
    )


@pytest.mark.asyncio
async def test_insert_scan(mocker, mock_db, mock_scan, mock_user):

    mock_db.execute.return_value = {
        "id": uuid4(),
        "url": "www.test.scan",
        "user_id": mock_user.id,
        "created_at": datetime.now(),
        "scrap_result": None,
        "scrapped_at": None,
        "analysis_result": None,
        "analyzed_at": None,
    }

    mocker.patch("app.repositories.scan.get_db", return_value = mock_db)

    new_scan = await insert_scan(mock_scan)

    assert isinstance(new_scan, Scan)
    assert new_scan is not None


@pytest.mark.asyncio
async def test_fetch_scan_by_id(mocker, mock_db, mock_scan, mock_user):
    
    mock_db.fetch_one.return_value = {
        "id": uuid4(),
        "url": "www.test.scan",
        "user_id": mock_user.id,
        "created_at": datetime.now(),
        "scrap_result": None,
        "scrapped_at": None,
        "analysis_result": None,
        "analyzed_at": None,
    }

    mocker.patch("app.repositories.scan.get_db", return_value = mock_db)

    scan = await fetch_scan_by_id(uuid4())

    assert scan is not None
    assert isinstance(scan, Scan)


@pytest.mark.asyncio
async def test_fetch_scans_by_user_id(mocker, mock_db, mock_scan, mock_user):
    
    mock_db.fetch_all.return_value = [{
        "id": uuid4(),
        "url": "www.test.scan",
        "user_id": mock_user.id,
        "created_at": datetime.now(),
        "scrap_result": None,
        "scrapped_at": None,
        "analysis_result": None,
        "analyzed_at": None,
    }]

    mocker.patch("app.repositories.scan.get_db", return_value = mock_db)

    scans = await fetch_scans_by_user_id(uuid4())

    assert scans is not None
    assert len(scans) == 1


@pytest.mark.asyncio
async def test_update_scrap_results(mocker, mock_db, mock_scan, mock_user):
    mock_db.execute.return_value = {
        "id": uuid4(),
        "url": "www.test.scan",
        "user_id": mock_user.id,
        "created_at": datetime.now(),
        "scrap_result": {
            "title": "test title",
            "content": "this is the content"
        },
        "scrapped_at": datetime.now(),
        "analysis_result": None,
        "analyzed_at": None,
    } # Not needed here

    mocker.patch("app.repositories.scan.get_db", return_value = mock_db)

    await update_scrap_result(mock_scan.id, ScrapResult(title="test title",content="this is the content"))  

    mock_db.execute.assert_awaited_once()



@pytest.mark.asyncio
async def test_update_analysis_results(mocker, mock_db, mock_scan):
    mock_db.execute.return_value = {}

    mocker.patch("app.repositories.scan.get_db", return_value = mock_db)

    await update_scrap_result(mock_scan.id, ScrapResult(title="test title",content="this is the content"))  

    mock_db.execute.assert_awaited_once()
