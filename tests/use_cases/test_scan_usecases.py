from datetime import datetime
from uuid import uuid4
import pytest

from app.core.entities.scan import AnalysisResult, Scan, ScrapeResult
from app.core.use_cases.scan import create_scan, get_scan_by_id, get_scans_by_user_id, save_analysis_result, save_scrape_result


    
@pytest.fixture
def mock_scan() -> Scan:
    return Scan(
        id=uuid4(),
        user_id=uuid4(),
        url="https://example.com",
        created_at=datetime.now()
    )


@pytest.mark.asyncio
async def test_create_scan(mocker, mock_scan):
    mock_repo = mocker.patch("app.core.use_cases.scan.insert_scan")
    mock_repo.return_value = mock_scan

    new_scan = await create_scan(mock_scan)

    mock_repo.assert_awaited_once()
    assert new_scan is not None
    assert new_scan.url == mock_scan.url


@pytest.mark.asyncio
async def test_get_scans(mocker, mock_scan):
    mock_repo = mocker.patch("app.core.use_cases.scan.fetch_scans_by_user_id")
    mock_repo.return_value = [
        mock_scan
    ]

    scans = await get_scans_by_user_id(mock_scan.user_id)

    mock_repo.assert_awaited_once_with(mock_scan.user_id)
    assert len(scans) == 1

    
@pytest.mark.asyncio
async def test_get_scan_by_id(mocker, mock_scan):
    mock_repo = mocker.patch("app.core.use_cases.scan.fetch_scan_by_id")
    mock_repo.return_value = mock_scan

    scan = await get_scan_by_id(mock_scan.id)

    mock_repo.assert_awaited_once_with(mock_scan.id)
    assert scan is not None
    assert scan.url == mock_scan.url


@pytest.mark.asyncio
async def test_save_scrape_result(mocker, mock_scan):
    mock_repo = mocker.patch("app.core.use_cases.scan.update_scrape_result")
    scrape_result = ScrapeResult(
        title="Example Page Title",
        content='"This is an example paragraph."'
    )
    mock_scan.scrape_result = scrape_result

    await save_scrape_result(mock_scan.id, scrape_result)

    mock_repo.assert_awaited_once_with(mock_scan.id, scrape_result)


@pytest.mark.asyncio
async def test_save_analysis_result(mocker, mock_scan):    
    mock_repo = mocker.patch("app.core.use_cases.scan.update_analysis_result")
    analysis_result =AnalysisResult(
        summary="This page discusses example topics.",
        tags=["example", "test", "demo"]
    )
    mock_scan.analysis_result = analysis_result

    await save_analysis_result(mock_scan.id, analysis_result)

    mock_repo.assert_awaited_once_with(mock_scan.id, analysis_result)

