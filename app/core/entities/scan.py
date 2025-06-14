from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


class ScrapeResult(BaseModel):
    title: str
    content: str


class AnalysisResult(BaseModel):
    summary: str
    tags: List[str]


class Scan(BaseModel):
    id: Optional[UUID] = None
    user_id: UUID
    url: str
    created_at: datetime
    scrape_result: Optional[ScrapeResult] = None
    scraped_at: Optional[datetime] = None
    analysis_result: Optional[AnalysisResult] = None
    analyzed_at: Optional[datetime] = None

    