"""
Skill gap analysis and recommendation routes for SmartResume AI.

Provides deep skill gap comparison between resumes and target job roles,
personalized recommendations, and analysis history tracking with MongoDB persistence.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.config.database import get_collection
from app.utils.helpers import extract_keywords_from_text, normalize_skill
from app.utils.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analysis", tags=["Analysis"])


def serialize_analysis(doc: dict) -> dict:
    """Convert MongoDB ObjectId to string ID."""
    if not doc:
        return {}
    res = dict(doc)
    if "_id" in res:
        res["id"] = str(res.pop("_id"))
    elif "id" not in res:
        res["id"] = ""
    return res


def extract_skills_from_resume_doc(resume_doc: dict) -> List[str]:
    """Extract and normalize all skills from a resume document."""
    skills = set()
    raw_skills = resume_doc.get("skills", [])
    if isinstance(raw_skills, list):
        for s in raw_skills:
            if isinstance(s, str) and s.strip():
                skills.add(normalize_skill(s.strip()))
            elif isinstance(s, dict) and "name" in s:
                skills.add(normalize_skill(str(s["name"]).strip()))

    text_corpus = f"{resume_doc.get('title', '')} {resume_doc.get('summary', '')}"
    for k in extract_keywords_from_text(text_corpus):
        skills.add(normalize_skill(k))

    return list(skills)


@router.post("/skill-gap")
async def analyze_skill_gap(
    body: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Perform a comprehensive skill gap analysis comparing a resume with a target job description.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    resume_id = body.get("resume_id") or body.get("resumeId") or ""
    job_description = body.get("job_description") or body.get("jobDescription") or ""

    if not resume_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="resume_id is required"
        )
    if not job_description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="job_description is required"
        )

    resumes_col = get_collection("resumes")
    r_query = {"_id": ObjectId(resume_id)} if ObjectId.is_valid(resume_id) else {"_id": resume_id}
    resume_doc = await resumes_col.find_one({"$and": [r_query, {"user_id": user_id}]})

    if not resume_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    resume_skills = set(extract_skills_from_resume_doc(resume_doc))
    job_keywords = extract_keywords_from_text(job_description)

    matching_skills = [k for k in job_keywords if k.lower() in {s.lower() for s in resume_skills}]
    missing_skills = [k for k in job_keywords if k.lower() not in {s.lower() for s in resume_skills}]

    gap_score = 0.0
    if job_keywords:
        gap_score = round((len(missing_skills) / len(job_keywords)) * 100, 1)

    match_percentage = 100.0 - gap_score

    recommendations = []
    if missing_skills:
        top_missing = missing_skills[:5]
        recommendations.append(f"Add critical missing skills to your resume: {', '.join(top_missing)}.")
        recommendations.append("Consider taking a short online course or project to demonstrate proficiency in missing areas.")
    if match_percentage >= 75:
        recommendations.append("Strong candidate profile! Emphasize leadership and measurable outcomes in recent projects.")
    else:
        recommendations.append("Customize your bullet points to directly reflect responsibilities listed in the job post.")

    now = datetime.now(timezone.utc).isoformat()
    analysis_record = {
        "user_id": user_id,
        "resume_id": resume_id,
        "job_description": job_description,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "gap_score": gap_score,
        "match_percentage": match_percentage,
        "recommendations": recommendations,
        "type": "skill_gap",
        "created_at": now,
    }

    analyses_col = get_collection("job_analyses")
    await analyses_col.insert_one(analysis_record)

    return {
        "status": "success",
        "data": {
            "missing_skills": missing_skills,
            "matching_skills": matching_skills,
            "gap_score": gap_score,
            "match_percentage": match_percentage,
            "recommendations": recommendations,
        }
    }


@router.get("/recommendations/{resume_id}")
async def get_resume_recommendations(
    resume_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Get personalized recommendations and actionable improvement areas for a specific resume.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    resumes_col = get_collection("resumes")

    r_query = {"_id": ObjectId(resume_id)} if ObjectId.is_valid(resume_id) else {"_id": resume_id}
    resume_doc = await resumes_col.find_one({"$and": [r_query, {"user_id": user_id}]})

    if not resume_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    # Gather past skill gap analyses for this resume
    analyses_col = get_collection("job_analyses")
    recent_analyses = await analyses_col.find(
        {"user_id": user_id, "resume_id": resume_id}
    ).sort("created_at", -1).to_list(length=10)

    top_missing_skills = set()
    for a in recent_analyses:
        for ms in a.get("missing_skills", []):
            top_missing_skills.add(ms)

    top_skills_to_add = list(top_missing_skills)[:8]

    recommendations = [
        "Include active action verbs (e.g., 'Engineered', 'Optimized', 'Led') at the start of experience bullet points.",
        "Quantify your accomplishments with metrics (e.g., 'Increased performance by 35%').",
        "Keep resume formatting clean and section headings standard for optimal ATS parsing.",
    ]

    if top_skills_to_add:
        recommendations.append(f"Frequently missing skills across target jobs: {', '.join(top_skills_to_add[:4])}.")

    career_advice = [
        "Align your LinkedIn profile headline with your target job title.",
        "Highlight hands-on project work or open source contributions if transitioning to a new tech stack.",
    ]

    return {
        "status": "success",
        "data": {
            "recommendations": recommendations,
            "top_skills_to_add": top_skills_to_add,
            "career_advice": career_advice,
        }
    }


@router.get("/history")
async def get_analysis_history(
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Retrieve historical job match and skill gap analyses for the current user.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    analyses_col = get_collection("job_analyses")

    cursor = analyses_col.find({"user_id": user_id}).sort("created_at", -1)
    docs = await cursor.to_list(length=200)
    serialized = [serialize_analysis(doc) for doc in docs]

    return {
        "status": "success",
        "data": serialized,
        "history": serialized,
    }
