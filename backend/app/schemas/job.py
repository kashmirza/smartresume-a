from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class JobAnalyzeRequest(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    job_description: str = Field(..., min_length=10)


class JobMatchRequest(BaseModel):
    resume_id: str
