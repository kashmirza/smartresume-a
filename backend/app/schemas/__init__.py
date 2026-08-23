"""
Schemas package for SmartResume AI.
"""

from .user_schema import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
)
from .resume_schema import (
    PersonalInfoSchema,
    EducationItemSchema,
    SkillsInfoSchema,
    ExperienceItemSchema,
    ProjectItemSchema,
    CertificationItemSchema,
    LanguageItemSchema,
    VolunteerItemSchema,
    PublicationItemSchema,
    ReferenceItemSchema,
    ResumeCreate,
    ResumeUpdate,
    ResumeResponse,
)
from .job_schema import (
    ExtractedSkillsSchema,
    JobCreate,
    JobResponse,
    JobAnalysisResponse,
)
from .analysis_schema import (
    ATSAnalysisRequest,
    ATSScoreBreakdownSchema,
    ATSScoreSchema,
    SkillGapSchema,
    SkillGapsPrioritySchema,
    RecommendationSchema,
    ATSAnalysisResponse,
    JobMatchResponse,
    SkillGapResponse,
    RecommendationResponse,
)

__all__ = [
    # User Schemas
    "UserCreate",
    "UserLogin",
    "UserUpdate",
    "UserResponse",
    # Resume Schemas
    "PersonalInfoSchema",
    "EducationItemSchema",
    "SkillsInfoSchema",
    "ExperienceItemSchema",
    "ProjectItemSchema",
    "CertificationItemSchema",
    "LanguageItemSchema",
    "VolunteerItemSchema",
    "PublicationItemSchema",
    "ReferenceItemSchema",
    "ResumeCreate",
    "ResumeUpdate",
    "ResumeResponse",
    # Job Schemas
    "ExtractedSkillsSchema",
    "JobCreate",
    "JobResponse",
    "JobAnalysisResponse",
    # Analysis Schemas
    "ATSAnalysisRequest",
    "ATSScoreBreakdownSchema",
    "ATSScoreSchema",
    "SkillGapSchema",
    "SkillGapsPrioritySchema",
    "RecommendationSchema",
    "ATSAnalysisResponse",
    "JobMatchResponse",
    "SkillGapResponse",
    "RecommendationResponse",
]
