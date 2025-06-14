from datetime import datetime
import json
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest

from app.core.entities.scan import AnalysisResult, Scan, ScrapeResult
from app.core.entities.user import User
from app.repositories.scan import fetch_scans_by_user_id, fetch_scan_by_id, insert_scan, update_scrape_result, update_analysis_result
from app.sql.scan import UPDATE_ANALYSIS_RESULT, UPDATE_SCRAPE_RESULT


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
async def test_update_scraped_results(mocker, mock_db, mock_scan, mock_user):
    mocker.patch("app.repositories.scan.get_db", return_value = mock_db)

    scrape_result = ScrapeResult(title="test title", content="this is the content")
    await update_scrape_result(mock_scan.id, scrape_result)  

    mock_db.execute.assert_awaited_once_with(
        UPDATE_SCRAPE_RESULT,
        {
            "id": str(mock_scan.id),
            "scrape_result_json": scrape_result.model_dump_json()
        }
    )



@pytest.mark.asyncio
async def test_update_analysis_results(mocker, mock_db, mock_scan):
    mocker.patch("app.repositories.scan.get_db", return_value = mock_db)

    analysis_result = AnalysisResult(summary="test title", tags=["web"])
    await update_analysis_result(mock_scan.id, analysis_result)  

    mock_db.execute.assert_awaited_once_with(
        UPDATE_ANALYSIS_RESULT,
        {
            "id": str(mock_scan.id),
            "analysis_result_json": analysis_result.model_dump_json()
        }
    )
