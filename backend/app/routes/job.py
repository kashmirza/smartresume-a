from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/jobs", tags=["Jobs"])


class JobCreateSchema(BaseModel):
    title: str
    company: str
    description: str
    requirements: List[str] = []
    location: Optional[str] = None


@router.get("/")
async def list_jobs():
    """
    List all job descriptions saved or imported by the user.
    """
    return {
        "status": "success",
        "jobs": []
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_job(job: JobCreateSchema):
    """
    Save or import a new job description.
    """
    return {
        "status": "success",
        "message": "Job created successfully",
        "job": job.dict()
    }


@router.get("/{job_id}")
async def get_job(job_id: str):
    """
    Get detailed job description and requirements.
    """
    return {
        "status": "success",
        "job_id": job_id,
        "data": {}
    }
