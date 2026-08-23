from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
async def get_dashboard_summary():
    """
    Get aggregated dashboard statistics including total resumes, saved jobs, and average match scores.
    """
    return {
        "status": "success",
        "data": {
            "total_resumes": 0,
            "total_jobs": 0,
            "avg_match_score": 0,
            "recent_analyses": []
        }
    }
