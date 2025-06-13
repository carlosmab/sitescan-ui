from uuid import UUID
from app.core.entities.scan import AnalysisResult, Scan, ScrapResult
from app.db import get_db
from app.sql.scan import FETCH_SCANS_BY_ID, FETCH_SCANS_BY_USER_ID, INSERT_SCAN, UPDATE_ANALYSIS_RESULT, UPDATE_SCRAP_RESULT



async def insert_scan(scan: Scan) -> Scan | None:
    result = await get_db().execute(INSERT_SCAN, scan.model_dump(exclude={"id", "created_at", "scrapped_at", "analyzed_at"}))
    return Scan.model_validate(dict(result)) if result else None


async def fetch_scans_by_user_id(user_id: UUID) -> list[Scan]:
    results = await get_db().fetch_all(FETCH_SCANS_BY_USER_ID, {"user_id": user_id})
    return [Scan.model_validate(dict(r)) for r in results]


async def fetch_scan_by_id(id: UUID) -> Scan | None:
    result = await get_db().fetch_one(FETCH_SCANS_BY_ID, {"id": id})
    return Scan.model_validate(result) if result else None


async def update_scrap_result(id: UUID, scrap_result: ScrapResult) -> None:
    await get_db().execute(UPDATE_SCRAP_RESULT, {"id": id, "scrap_result": scrap_result.model_dump_json}) 


async def update_analysis_result(id: UUID, analysis_result: AnalysisResult) -> None:
    await get_db().execute(UPDATE_ANALYSIS_RESULT, {"id": id, "Analysis_result": analysis_result.model_dump_json}) 