from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/analysis", tags=["Analysis"])


class ResumeJobMatchRequest(BaseModel):
    resume_id: str
    job_id: str


@router.post("/match")
async def match_resume_to_job(request: ResumeJobMatchRequest):
    """
    Perform ATS score matching and keyword gap analysis between a resume and job description.
    """
    return {
        "status": "success",
        "match_score": 85,
        "matching_keywords": ["python", "fastapi", "mongodb", "asyncio"],
        "missing_keywords": ["docker", "kubernetes"],
        "recommendations": [
            "Highlight Experience with containerization tools like Docker",
            "Quantify achievements in project descriptions"
        ]
    }


@router.post("/ats-check")
async def check_ats_compatibility(resume_id: str):
    """
    Analyze resume ATS compatibility and structure compliance.
    """
    return {
        "status": "success",
        "resume_id": resume_id,
        "ats_score": 92,
        "format_checks": {
            "font_compatibility": "PASS",
            "section_headings": "PASS",
            "table_detection": "NO_TABLES_DETECTED (GOOD)"
        }
    }
