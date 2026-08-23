from app.routes.auth import router as auth_router
from app.routes.resume import router as resume_router
from app.routes.job import router as job_router
from app.routes.analysis import router as analysis_router
from app.routes.dashboard import router as dashboard_router

__all__ = [
    "auth_router",
    "resume_router",
    "job_router",
    "analysis_router",
    "dashboard_router",
]
