"""
Models package for SmartResume AI.
"""

from .user import User, CareerLevel
from .resume import (
    Resume,
    PersonalInfo,
    EducationItem,
    SkillsInfo,
    ExperienceItem,
    ProjectItem,
    CertificationItem,
    LanguageItem,
    VolunteerItem,
    PublicationItem,
    ReferenceItem,
)
from .job import Job, ExtractedSkills
from .analysis import (
    Analysis,
    ATSScore,
    ATSScoreBreakdown,
    SkillGap,
    SkillGapsPriority,
    Recommendation,
    PriorityLevel,
)

__all__ = [
    "User",
    "CareerLevel",
    "Resume",
    "PersonalInfo",
    "EducationItem",
    "SkillsInfo",
    "ExperienceItem",
    "ProjectItem",
    "CertificationItem",
    "LanguageItem",
    "VolunteerItem",
    "PublicationItem",
    "ReferenceItem",
    "Job",
    "ExtractedSkills",
    "Analysis",
    "ATSScore",
    "ATSScoreBreakdown",
    "SkillGap",
    "SkillGapsPriority",
    "Recommendation",
    "PriorityLevel",
]
