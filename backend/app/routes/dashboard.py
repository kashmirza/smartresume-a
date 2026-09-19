"""
Dashboard metrics and analytics routes for SmartResume AI.

Provides aggregated statistics for total resumes, jobs analyzed, average ATS score,
and recent user analysis history.
"""

import logging
from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.config.database import get_collection
from app.utils.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


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


@router.get("/stats")
async def get_dashboard_stats(
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Retrieve overview statistics for the current user's dashboard.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))

    resumes_col = get_collection("resumes")
    jobs_col = get_collection("jobs")
    analyses_col = get_collection("job_analyses")

    # Total Resumes Count
    total_resumes = await resumes_col.count_documents({"user_id": user_id})

    # Total Jobs Count
    total_jobs = await jobs_col.count_documents({"user_id": user_id})

    # Average ATS Score
    resumes_cursor = resumes_col.find({"user_id": user_id, "ats_score": {"$exists": True}})
    resumes_list = await resumes_cursor.to_list(length=500)

    if resumes_list:
        scores = [float(r.get("ats_score", 0.0)) for r in resumes_list if r.get("ats_score") is not None]
        avg_ats_score = round(sum(scores) / len(scores), 1) if scores else 75.0
    else:
        avg_ats_score = 75.0

    # Recent Analyses
    recent_cursor = analyses_col.find({"user_id": user_id}).sort("created_at", -1).limit(5)
    recent_docs = await recent_cursor.to_list(length=5)
    recent_analyses = [serialize_analysis(d) for d in recent_docs]

    stats_payload = {
        "total_resumes": total_resumes,
        "totalResumes": total_resumes,
        "total_jobs": total_jobs,
        "totalJobs": total_jobs,
        "avg_ats_score": avg_ats_score,
        "avgAtsScore": avg_ats_score,
        "recent_analyses": recent_analyses,
        "recentAnalyses": recent_analyses,
    }

    return {
        "status": "success",
        "data": stats_payload,
    }
