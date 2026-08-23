import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.settings import settings
from app.config.database import connect_to_mongo, close_mongo_connection, db
from app.routes import (
    auth_router,
    resume_router,
    job_router,
    analysis_router,
    dashboard_router,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("smartresume.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager handling startup and shutdown tasks.
    """
    logger.info("Starting up SmartResume AI Backend API...")
    await connect_to_mongo()
    yield
    logger.info("Shutting down SmartResume AI Backend API...")
    await close_mongo_connection()


# Initialize FastAPI application
app = FastAPI(
    title="SmartResume AI Backend API",
    description="ATS Resume Builder + AI Job Matcher core API powered by FastAPI, Motor (MongoDB), and Spacy NLP.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers under /api/v1
app.include_router(auth_router, prefix="/api")
app.include_router(resume_router, prefix="/api")
app.include_router(job_router, prefix="/api")
app.include_router(analysis_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint returning API status and version metadata.
    """
    return {
        "app": "SmartResume AI Backend",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs",
        "api_v1": "/api/v1"
    }


@app.get("/health", tags=["Health Check"])
@app.get("/api/health", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint reporting application and database connectivity status.
    """
    db_status = "disconnected"
    if db.client is not None:
        try:
            await db.client.admin.command("ping")
            db_status = "connected"
        except Exception as e:
            logger.warning("Database ping failed during health check: %s", e)
            db_status = "error"

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "database": db_status,
            "database_name": settings.DATABASE_NAME,
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=(settings.ENVIRONMENT == "development"),
    )
