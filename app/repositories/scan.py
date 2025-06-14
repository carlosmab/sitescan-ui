from uuid import UUID
from app.core.entities.scan import AnalysisResult, Scan, ScrapeResult
from app.db import get_db
from app.sql.scan import FETCH_SCANS_BY_ID, FETCH_SCANS_BY_USER_ID, INSERT_SCAN, UPDATE_ANALYSIS_RESULT, UPDATE_SCRAPE_RESULT



async def insert_scan(scan: Scan) -> Scan | None:
    result = await get_db().execute(INSERT_SCAN, scan.model_dump(exclude={"id", "created_at", "scrapped_at", "analyzed_at"}))
    return Scan.model_validate(dict(result)) if result else None


async def fetch_scans_by_user_id(user_id: UUID) -> list[Scan]:
    results = await get_db().fetch_all(FETCH_SCANS_BY_USER_ID, {"user_id": user_id})
    return [Scan.model_validate(dict(r)) for r in results]


async def fetch_scan_by_id(id: UUID) -> Scan | None:
    result = await get_db().fetch_one(FETCH_SCANS_BY_ID, {"id": id})
    return Scan.model_validate(result) if result else None


async def update_scrape_result(scan_id: UUID, scrape_result: ScrapeResult) -> None:
    await get_db().execute(UPDATE_SCRAPE_RESULT, {"id": str(scan_id), "scrape_result_json": scrape_result.model_dump_json()}) 


async def update_analysis_result(scan_id: UUID, analysis_result: AnalysisResult) -> None:
    await get_db().execute(UPDATE_ANALYSIS_RESULT, {"id": str(scan_id), "analysis_result_json": analysis_result.model_dump_json()}) 