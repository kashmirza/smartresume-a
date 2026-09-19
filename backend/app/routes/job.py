"""
Job description analysis and matching routes for SmartResume AI.

Extracts technical skills and requirements from job postings, provides CRUD operations for jobs,
and performs skill matching against user resumes with MongoDB persistence.
"""

from datetime import datetime, timezone
import logging
import re
from typing import Any, Dict, List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.config.database import get_collection
from app.utils.helpers import extract_keywords_from_text, normalize_skill
from app.utils.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["Jobs"])


def serialize_job(doc: dict) -> dict:
    """Convert MongoDB document ObjectId to string ID."""
    if not doc:
        return {}
    res = dict(doc)
    if "_id" in res:
        res["id"] = str(res.pop("_id"))
    elif "id" not in res:
        res["id"] = ""
    return res


def build_job_query(job_id: str, user_id: str) -> dict:
    """Construct query for job matching ID and user isolation."""
    id_filter = {"_id": ObjectId(job_id)} if ObjectId.is_valid(job_id) else {"_id": job_id}
    return {"$and": [id_filter, {"user_id": user_id}]}


def extract_skills_from_text_regex(text: str) -> List[str]:
    """Extract technical keywords from text using helper and regex patterns."""
    keywords = extract_keywords_from_text(text)
    normalized = list(dict.fromkeys([normalize_skill(k) for k in keywords if k]))
    return normalized


def extract_title_and_company(text: str) -> Dict[str, str]:
    """Extract approximate job title and company from description text."""
    title = "Target Position"
    company = "Hiring Organization"

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if lines:
        first_line = lines[0]
        if len(first_line) < 80:
            title = first_line

    title_match = re.search(r"(?:Title|Role|Position)\s*:\s*([^\n\r]+)", text, re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()

    company_match = re.search(r"(?:Company|Organization|Employer)\s*:\s*([^\n\r]+)", text, re.IGNORECASE)
    if company_match:
        company = company_match.group(1).strip()

    return {"title": title, "company": company}


@router.post("/analyze", status_code=status.HTTP_201_CREATED)
async def analyze_job(
    body: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Analyze job description text, extract key technical skills and requirements, and store in jobs collection.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    job_description = body.get("job_description") or body.get("jobDescription") or body.get("description") or ""

    if not job_description or not job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="job_description string is required"
        )

    meta = extract_title_and_company(job_description)
    title = body.get("title") or meta["title"]
    company = body.get("company") or meta["company"]

    extracted_keywords = extract_skills_from_text_regex(job_description)

    now = datetime.now(timezone.utc).isoformat()
    job_doc = {
        "user_id": user_id,
        "title": title,
        "company": company,
        "job_description": job_description,
        "skills": extracted_keywords,
        "keywords": extracted_keywords,
        "requirements": extracted_keywords[:10],
        "created_at": now,
        "updated_at": now,
    }

    jobs_col = get_collection("jobs")
    result = await jobs_col.insert_one(job_doc)
    job_id = str(result.inserted_id)

    job_doc["id"] = job_id
    if "_id" in job_doc:
        del job_doc["_id"]

    return {
        "status": "success",
        "id": job_id,
        "data": job_doc,
        "job": job_doc,
    }


@router.get("/")
@router.get("", include_in_schema=False)
async def list_jobs(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    List all job descriptions saved or analyzed by the current user.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    jobs_col = get_collection("jobs")

    cursor = jobs_col.find({"user_id": user_id}).sort("created_at", -1)
    docs = await cursor.to_list(length=500)
    serialized = [serialize_job(doc) for doc in docs]

    return {
        "status": "success",
        "data": serialized,
        "jobs": serialized,
    }


@router.get("/{job_id}")
async def get_job(
    job_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Retrieve details of a specific job posting by ID.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    jobs_col = get_collection("jobs")

    query = build_job_query(job_id, user_id)
    doc = await jobs_col.find_one(query)

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    serialized = serialize_job(doc)
    return {
        "status": "success",
        "data": serialized,
        "job": serialized,
    }


@router.post("/match")
async def match_resume_to_job(
    body: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Compare resume skills against job requirements and return match score and recommendations.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    resume_id = body.get("resume_id") or body.get("resumeId") or ""
    job_description = body.get("job_description") or body.get("jobDescription") or ""
    job_id = body.get("job_id") or body.get("jobId") or ""

    if not resume_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="resume_id is required"
        )

    # Retrieve resume
    resumes_col = get_collection("resumes")
    r_query = {"_id": ObjectId(resume_id)} if ObjectId.is_valid(resume_id) else {"_id": resume_id}
    resume_doc = await resumes_col.find_one({"$and": [r_query, {"user_id": user_id}]})

    if not resume_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    # Determine job description
    if not job_description and job_id:
        jobs_col = get_collection("jobs")
        j_query = build_job_query(job_id, user_id)
        job_doc = await jobs_col.find_one(j_query)
        if job_doc:
            job_description = job_doc.get("job_description", "")

    if not job_description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="job_description or valid job_id is required"
        )

    # Extract resume skills
    resume_skills = set()
    raw_r_skills = resume_doc.get("skills", [])
    if isinstance(raw_r_skills, list):
        for item in raw_r_skills:
            if isinstance(item, str):
                resume_skills.add(normalize_skill(item.strip()))
            elif isinstance(item, dict) and "name" in item:
                resume_skills.add(normalize_skill(str(item["name"]).strip()))

    r_text_keywords = extract_keywords_from_text(
        f"{resume_doc.get('title', '')} {resume_doc.get('summary', '')}"
    )
    for k in r_text_keywords:
        resume_skills.add(normalize_skill(k))

    # Extract job skills
    job_skills = extract_skills_from_text_regex(job_description)

    matching_skills = [s for s in job_skills if s.lower() in {rs.lower() for s in resume_skills}]
    missing_skills = [s for s in job_skills if s.lower() not in {rs.lower() for s in resume_skills}]

    match_score = 0.0
    if job_skills:
        match_score = round((len(matching_skills) / len(job_skills)) * 100, 1)

    recommendations = []
    if missing_skills:
        recommendations.append(f"Add critical missing skills to your resume: {', '.join(missing_skills[:5])}")
    if match_score < 60:
        recommendations.append("Consider revising your summary to reflect key phrases from the job description.")
    else:
        recommendations.append("High skill overlap! Make sure your work experience highlights recent usage of these skills.")

    # Store analysis record in job_analyses
    analyses_col = get_collection("job_analyses")
    now = datetime.now(timezone.utc).isoformat()

    analysis_record = {
        "user_id": user_id,
        "resume_id": resume_id,
        "job_id": job_id,
        "job_description": job_description,
        "match_score": match_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations,
        "type": "job_match",
        "created_at": now,
    }

    await analyses_col.insert_one(analysis_record)

    return {
        "status": "success",
        "data": {
            "match_score": match_score,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "recommendations": recommendations,
        }
    }


@router.delete("/{job_id}")
async def delete_job(
    job_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Delete a saved job posting by ID.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    jobs_col = get_collection("jobs")

    query = build_job_query(job_id, user_id)
    result = await jobs_col.delete_one(query)

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    return {
        "status": "success",
        "message": "Job deleted successfully"
    }
