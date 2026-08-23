from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SkillGapRequest(BaseModel):
    resume_id: Optional[str] = None
    job_id: Optional[str] = None
    job_description: Optional[str] = None
    resume_skills: Optional[List[str]] = None
    target_skills: Optional[List[str]] = None
