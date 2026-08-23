"""
Analysis model for SmartResume AI ATS evaluator.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
import uuid

from pydantic import BaseModel, ConfigDict, Field


class PriorityLevel(str, Enum):
    """Priority classification for skill gaps and recommendations."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ATSScoreBreakdown(BaseModel):
    """Detailed score breakdown across ATS criteria."""
    keyword_match_score: float = Field(
        ..., ge=0.0, le=100.0, description="Score based on keyword overlap (0-100)"
    )
    skill_match_score: float = Field(
        ..., ge=0.0, le=100.0, description="Score based on required and preferred skills match (0-100)"
    )
    experience_match_score: float = Field(
        ..., ge=0.0, le=100.0, description="Score based on experience alignment (0-100)"
    )
    education_match_score: float = Field(
        ..., ge=0.0, le=100.0, description="Score based on education criteria match (0-100)"
    )
    formatting_score: float = Field(
        ..., ge=0.0, le=100.0, description="Score based on ATS readability and formatting structure (0-100)"
    )

    model_config = ConfigDict(from_attributes=True)


class ATSScore(BaseModel):
    """Composite ATS score and breakdown."""
    overall: float = Field(
        ..., ge=0.0, le=100.0, description="Overall ATS compatibility score (0-100)"
    )
    breakdown: ATSScoreBreakdown = Field(
        ..., description="Granular breakdown of individual ATS evaluation dimensions"
    )

    model_config = ConfigDict(from_attributes=True)


class SkillGap(BaseModel):
    """Individual skill gap item with priority and learning resource recommendations."""
    skill: str = Field(..., description="Name of the missing or underrepresented skill")
    category: Optional[str] = Field(default=None, description="Domain category (e.g. Frontend, DevOps)")
    priority: PriorityLevel = Field(
        default=PriorityLevel.MEDIUM, description="Priority level to bridge this gap"
    )
    reason: Optional[str] = Field(
        default=None, description="Explanation of why this skill is critical for the role"
    )
    learning_resources: List[str] = Field(
        default_factory=list, description="Links or names of recommended learning resources"
    )

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class SkillGapsPriority(BaseModel):
    """Skill gaps categorized by priority level."""
    high: List[SkillGap] = Field(
        default_factory=list, description="High priority skill gaps requiring immediate focus"
    )
    medium: List[SkillGap] = Field(
        default_factory=list, description="Medium priority skill gaps to improve fit"
    )
    low: List[SkillGap] = Field(
        default_factory=list, description="Low priority skill gaps or nice-to-haves"
    )

    model_config = ConfigDict(from_attributes=True)


class Recommendation(BaseModel):
    """Actionable recommendation for resume optimization."""
    category: str = Field(
        ..., description="Section or area for improvement (e.g. 'Skills', 'Work Experience', 'Summary')"
    )
    title: str = Field(..., description="Short headline title of the recommendation")
    description: str = Field(..., description="Detailed explanation of what needs modification")
    actionable_steps: List[str] = Field(
        default_factory=list, description="Concrete step-by-step actions to execute"
    )

    model_config = ConfigDict(from_attributes=True)


class Analysis(BaseModel):
    """
    Analysis domain and database model.
    """
    analysis_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the analysis evaluation"
    )
    user_id: str = Field(..., description="ID of user requesting analysis")
    resume_id: str = Field(..., description="ID of resume being evaluated")
    job_id: str = Field(..., description="ID of job posting evaluated against")
    ats_score: ATSScore = Field(..., description="Overall ATS score and breakdown")
    matched_skills: List[str] = Field(
        default_factory=list, description="List of skills successfully matched"
    )
    missing_skills: List[str] = Field(
        default_factory=list, description="List of required skills missing from resume"
    )
    partial_skills: List[str] = Field(
        default_factory=list, description="List of partially matched or related skills"
    )
    match_score: float = Field(
        ..., ge=0.0, le=100.0, description="Overall match percentage score (0-100)"
    )
    skill_gaps: SkillGapsPriority = Field(
        default_factory=SkillGapsPriority, description="Categorized high/medium/low priority skill gaps"
    )
    recommendations: List[Recommendation] = Field(
        default_factory=list, description="Actionable recommendations to boost ATS score"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp when analysis was generated"
    )

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
