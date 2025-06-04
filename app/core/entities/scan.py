from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


class ScrapResult(BaseModel):
    title: str
    content: str


class AnalysisResult(BaseModel):
    summary: str
    frequent_words: List[str]


class Scan(BaseModel):
    id: Optional[UUID] = None
    user_id: UUID
    url: str
    created_at: datetime
    scrap_result: Optional[ScrapResult] = None
    scrapped_at: Optional[datetime] = None
    analysis_result: Optional[AnalysisResult] = None
    analyzed_at: Optional[datetime] = None

    