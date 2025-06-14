from uuid import UUID
from app.core.entities.scan import AnalysisResult, Scan, ScrapeResult
from app.repositories.scan import fetch_scan_by_id, insert_scan, fetch_scans_by_user_id, update_analysis_result, update_scrape_result


async def create_scan(scan: Scan) -> Scan | None:
    return await insert_scan(scan)


async def get_scans_by_user_id(user_id: UUID) -> list[Scan]:
    return await fetch_scans_by_user_id(user_id)


async def get_scan_by_id(scan_id: UUID) -> Scan | None:
    return await fetch_scan_by_id(scan_id)


async def save_scrape_result(scan_id: UUID, scrape_result: ScrapeResult) -> None:
    return await update_scrape_result(scan_id, scrape_result)


async def save_analysis_result(scan_id: UUID, analysis_result: AnalysisResult) -> None:
    return await update_analysis_result(scan_id, analysis_result)