"""
Resume management and analysis routes for SmartResume AI.

Provides full CRUD operations, ATS analysis scoring, job-specific resume optimization,
and resume download endpoints with MongoDB persistence and user isolation.
"""

from datetime import datetime, timezone
import logging
import re
from typing import Any, Dict, List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response

from app.config.database import get_collection
from app.utils.helpers import extract_keywords_from_text, normalize_skill
from app.utils.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/resumes", tags=["Resumes"])


def build_resume_query(resume_id: str, user_id: str) -> dict:
    """Construct MongoDB query for a resume matching ID and user isolation."""
    id_filter = {"_id": ObjectId(resume_id)} if ObjectId.is_valid(resume_id) else {"_id": resume_id}
    return {"$and": [id_filter, {"user_id": user_id}]}


def serialize_resume(doc: dict) -> dict:
    """Convert MongoDB document ObjectId to string ID for API response."""
    if not doc:
        return {}
    res = dict(doc)
    if "_id" in res:
        res["id"] = str(res.pop("_id"))
    elif "id" not in res:
        res["id"] = ""
    return res


def extract_skills_from_resume_dict(resume: dict) -> List[str]:
    """Extract a list of normalized skill strings from a resume dictionary."""
    skills_set = set()

    raw_skills = resume.get("skills", [])
    if isinstance(raw_skills, list):
        for item in raw_skills:
            if isinstance(item, str) and item.strip():
                skills_set.add(normalize_skill(item.strip()))
            elif isinstance(item, dict):
                s_name = item.get("name") or item.get("skill") or ""
                if s_name and isinstance(s_name, str):
                    skills_set.add(normalize_skill(s_name.strip()))

    # Extract text keywords from summary and title
    text_corpus = []
    if resume.get("summary"):
        text_corpus.append(str(resume["summary"]))
    if resume.get("title"):
        text_corpus.append(str(resume["title"]))
    if isinstance(resume.get("personal"), dict):
        p = resume["personal"]
        if p.get("jobTitle"):
            text_corpus.append(str(p["jobTitle"]))

    full_text = " ".join(text_corpus)
    if full_text.strip():
        extracted = extract_keywords_from_text(full_text)
        for k in extracted:
            skills_set.add(k)

    return list(skills_set)


def perform_ats_analysis(resume: dict) -> dict:
    """Evaluate resume structural completeness, skills count, and formatting for ATS scoring."""
    personal = resume.get("personal") or {}

    sections_status = {
        "contact_info": bool(personal.get("fullName") or personal.get("email") or personal.get("phone")),
        "summary": bool(resume.get("summary") and str(resume.get("summary")).strip()),
        "experience": bool(resume.get("experience") and isinstance(resume.get("experience"), list) and len(resume.get("experience")) > 0),
        "education": bool(resume.get("education") and isinstance(resume.get("education"), list) and len(resume.get("education")) > 0),
        "skills": bool(resume.get("skills") and isinstance(resume.get("skills"), list) and len(resume.get("skills")) > 0),
        "projects": bool(resume.get("projects") and isinstance(resume.get("projects"), list) and len(resume.get("projects")) > 0),
        "certifications": bool(resume.get("certifications") and isinstance(resume.get("certifications"), list) and len(resume.get("certifications")) > 0),
    }

    completeness_score = round((sum(1 for v in sections_status.values() if v) / len(sections_status)) * 100, 1)

    extracted_skills = extract_skills_from_resume_dict(resume)
    skills_count = len(extracted_skills)
    skills_score = min(100.0, round((skills_count / 8.0) * 100, 1))

    exp_list = resume.get("experience") or []
    exp_score = 0.0
    if isinstance(exp_list, list) and len(exp_list) > 0:
        detailed_count = 0
        for exp in exp_list:
            if isinstance(exp, dict) and (exp.get("description") or exp.get("highlights") or exp.get("responsibilities")):
                detailed_count += 1
        exp_score = min(100.0, round((detailed_count / len(exp_list)) * 100, 1))
    elif sections_status["experience"]:
        exp_score = 70.0

    overall_score = round(completeness_score * 0.4 + skills_score * 0.3 + exp_score * 0.3, 1)

    feedback = []
    if not sections_status["contact_info"]:
        feedback.append("Ensure your full name, email, and phone number are provided in personal contact info.")
    if not sections_status["summary"]:
        feedback.append("Add a compelling professional summary highlighting your key achievements and goals.")
    if skills_count < 5:
        feedback.append(f"Only {skills_count} skills detected. Add at least 6-10 technical and domain skills.")
    if not sections_status["experience"]:
        feedback.append("Include work experience entries with bullet points describing key responsibilities.")
    if not sections_status["projects"]:
        feedback.append("Add project details to demonstrate hands-on application of your skills.")
    if overall_score >= 80:
        feedback.append("Excellent structure! Your resume aligns well with standard ATS formatting guidelines.")

    return {
        "score": overall_score,
        "overall_score": overall_score,
        "feedback": feedback,
        "section_scores": {
            "completeness": completeness_score,
            "skills": skills_score,
            "experience": exp_score,
        },
        "details": {
            "sections_status": sections_status,
            "detected_skills_count": skills_count,
            "detected_skills": extracted_skills,
        }
    }


@router.get("/")
@router.get("", include_in_schema=False)
async def list_resumes(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    List all resumes owned by the currently authenticated user.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    resumes_col = get_collection("resumes")

    cursor = resumes_col.find({"user_id": user_id}).sort("updated_at", -1)
    docs = await cursor.to_list(length=500)
    serialized = [serialize_resume(doc) for doc in docs]

    return {
        "status": "success",
        "data": serialized,
        "resumes": serialized,
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
@router.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_resume(
    body: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Create a new resume document for the authenticated user. Accepts any JSON body.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    resumes_col = get_collection("resumes")

    now = datetime.now(timezone.utc).isoformat()

    doc = dict(body)
    doc["user_id"] = user_id
    doc["created_at"] = now
    doc["updated_at"] = now

    if "title" not in doc or not doc["title"]:
        p = doc.get("personal") if isinstance(doc.get("personal"), dict) else {}
        job_title = p.get("jobTitle") or "Untitled Resume"
        doc["title"] = f"{job_title} Resume"

    # Compute initial ATS score
    ats_res = perform_ats_analysis(doc)
    doc["ats_score"] = ats_res["overall_score"]

    result = await resumes_col.insert_one(doc)
    inserted_id = str(result.inserted_id)

    doc["id"] = inserted_id
    if "_id" in doc:
        del doc["_id"]

    return {
        "status": "success",
        "id": inserted_id,
        "data": doc,
        "resume": doc,
    }


@router.get("/{resume_id}")
async def get_resume(
    resume_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Retrieve details of a specific resume owned by the user.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    resumes_col = get_collection("resumes")

    query = build_resume_query(resume_id, user_id)
    doc = await resumes_col.find_one(query)

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    serialized = serialize_resume(doc)
    return {
        "status": "success",
        "data": serialized,
        "resume": serialized,
    }


@router.put("/{resume_id}")
async def update_resume(
    resume_id: str,
    body: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Update an existing resume document owned by the user. Accepts any JSON body.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    resumes_col = get_collection("resumes")

    query = build_resume_query(resume_id, user_id)
    existing = await resumes_col.find_one(query)

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    update_doc = dict(body)
    update_doc.pop("_id", None)
    update_doc.pop("id", None)
    update_doc["user_id"] = user_id
    update_doc["updated_at"] = datetime.now(timezone.utc).isoformat()

    # Recalculate ATS score
    ats_res = perform_ats_analysis(update_doc)
    update_doc["ats_score"] = ats_res["overall_score"]

    await resumes_col.update_one(query, {"$set": update_doc})

    updated_doc = await resumes_col.find_one(query)
    serialized = serialize_resume(updated_doc)

    return {
        "status": "success",
        "data": serialized,
        "resume": serialized,
    }


@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Delete a specific resume owned by the user.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    resumes_col = get_collection("resumes")

    query = build_resume_query(resume_id, user_id)
    result = await resumes_col.delete_one(query)

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    return {
        "status": "success",
        "message": "Resume deleted successfully"
    }


@router.post("/{resume_id}/ats-analysis")
async def resume_ats_analysis(
    resume_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Run full ATS evaluation and keyword scoring on a user's resume.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    resumes_col = get_collection("resumes")

    query = build_resume_query(resume_id, user_id)
    doc = await resumes_col.find_one(query)

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    analysis_res = perform_ats_analysis(doc)

    # Persist updated score on the resume document
    await resumes_col.update_one(
        query,
        {"$set": {"ats_score": analysis_res["overall_score"], "updated_at": datetime.now(timezone.utc).isoformat()}}
    )

    return {
        "status": "success",
        "data": analysis_res
    }


@router.post("/{resume_id}/optimize")
async def optimize_resume(
    resume_id: str,
    body: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Optimize resume against a provided job description by identifying keyword gaps and suggestions.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    resumes_col = get_collection("resumes")

    query = build_resume_query(resume_id, user_id)
    doc = await resumes_col.find_one(query)

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    job_description = body.get("job_description") or body.get("jobDescription") or ""
    if not job_description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="job_description is required for optimization"
        )

    resume_skills = set(extract_skills_from_resume_dict(doc))
    job_keywords = extract_keywords_from_text(job_description)

    matching_keywords = [k for k in job_keywords if k.lower() in {s.lower() for s in resume_skills}]
    missing_keywords = [k for k in job_keywords if k.lower() not in {s.lower() for s in resume_skills}]

    match_score = 0.0
    if job_keywords:
        match_score = round((len(matching_keywords) / len(job_keywords)) * 100, 1)

    suggestions = []
    if missing_keywords:
        top_missing = missing_keywords[:5]
        suggestions.append(f"Incorporate missing key terms: {', '.join(top_missing)}")
    if match_score < 70:
        suggestions.append("Tailor your summary and experience bullet points using exact phrasing from the job description.")
    else:
        suggestions.append("Strong keyword alignment! Consider quantifying key achievements in your work history.")

    summary = doc.get("summary") or ""
    target_role = doc.get("title") or "Target Role"
    optimized_summary = f"{summary} Results-driven {target_role} experienced in {', '.join(matching_keywords[:4])}." if matching_keywords else summary

    return {
        "status": "success",
        "data": {
            "score": match_score,
            "match_score": match_score,
            "suggestions": suggestions,
            "missing_keywords": missing_keywords,
            "matching_keywords": matching_keywords,
            "optimized_summary": optimized_summary,
        }
    }


@router.get("/{resume_id}/download")
async def download_resume(
    resume_id: str,
    template: str = Query("ats_classic"),
    format: str = Query("pdf"),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Download endpoint for a resume. Returns a JSON response containing resume data and metadata.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    resumes_col = get_collection("resumes")

    query = build_resume_query(resume_id, user_id)
    doc = await resumes_col.find_one(query)

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    serialized = serialize_resume(doc)

    # Generate a real PDF file from the resume data
    try:
        from app.services.pdf_generator import generate_pdf
        import io
        pdf_bytes = generate_pdf(serialized, template)
        safe_title = re.sub(r"[^A-Za-z0-9_-]+", "_", serialized.get("title") or "resume").strip("_") or "resume"
        filename = f"{safe_title}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as exc:
        logger.error("PDF generation failed: %s", exc)
        # Fallback: return raw data as JSON if PDF generation unavailable
        return {
            "status": "success",
            "message": "PDF generation unavailable; returning raw data",
            "resume_id": resume_id,
            "template": template,
            "format": format,
            "data": serialized,
        }
