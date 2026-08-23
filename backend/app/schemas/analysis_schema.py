"""
Analysis schemas for API requests and responses.
"""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field

from ..models.analysis import PriorityLevel


class ATSAnalysisRequest(BaseModel):
    """Payload schema requesting ATS evaluation between a resume and job posting."""
    resume_id: str = Field(..., description="ID of the resume to evaluate")
    job_id: str = Field(..., description="ID of the job posting to match against")
    custom_weights: Optional[Dict[str, float]] = Field(
        default=None,
        description="Optional scoring weight overrides (e.g. {'skill_match': 0.4, 'keyword_match': 0.3})"
    )


class ATSScoreBreakdownSchema(BaseModel):
    """Schema for individual component scores in ATS calculation."""
    keyword_match_score: float = Field(..., ge=0.0, le=100.0, description="Keyword overlap score (0-100)")
    skill_match_score: float = Field(..., ge=0.0, le=100.0, description="Skills match score (0-100)")
    experience_match_score: float = Field(..., ge=0.0, le=100.0, description="Experience alignment score (0-100)")
    education_match_score: float = Field(..., ge=0.0, le=100.0, description="Education requirement match score (0-100)")
    formatting_score: float = Field(..., ge=0.0, le=100.0, description="ATS readability score (0-100)")

    model_config = ConfigDict(from_attributes=True)


class ATSScoreSchema(BaseModel):
    """Schema for overall ATS score and component breakdown."""
    overall: float = Field(..., ge=0.0, le=100.0, description="Composite ATS match score (0-100)")
    breakdown: ATSScoreBreakdownSchema = Field(..., description="Detailed breakdown by criteria")

    model_config = ConfigDict(from_attributes=True)


class SkillGapSchema(BaseModel):
    """Schema for individual identified skill gap."""
    skill: str = Field(..., description="Name of the missing or underrepresented skill")
    category: Optional[str] = Field(default=None, description="Category of the skill")
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM, description="Priority rating (high, medium, low)")
    reason: Optional[str] = Field(default=None, description="Reason why this skill is needed")
    learning_resources: List[str] = Field(default_factory=list, description="Suggested courses, docs, or materials")

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class SkillGapsPrioritySchema(BaseModel):
    """Schema for skill gaps grouped by priority level."""
    high: List[SkillGapSchema] = Field(default_factory=list, description="High priority skill gaps")
    medium: List[SkillGapSchema] = Field(default_factory=list, description="Medium priority skill gaps")
    low: List[SkillGapSchema] = Field(default_factory=list, description="Low priority skill gaps")

    model_config = ConfigDict(from_attributes=True)


class RecommendationSchema(BaseModel):
    """Schema for actionable ATS resume improvement recommendation."""
    category: str = Field(..., description="Target section for improvement")
    title: str = Field(..., description="Recommendation headline title")
    description: str = Field(..., description="Detailed guidance")
    actionable_steps: List[str] = Field(default_factory=list, description="Bullet points of concrete actions to perform")

    model_config = ConfigDict(from_attributes=True)


class ATSAnalysisResponse(BaseModel):
    """Complete response schema for an ATS evaluation analysis."""
    analysis_id: str = Field(..., description="Unique analysis record identifier")
    user_id: str = Field(..., description="User ID who owns this analysis")
    resume_id: str = Field(..., description="Resume ID evaluated")
    job_id: str = Field(..., description="Job ID evaluated against")
    ats_score: ATSScoreSchema = Field(..., description="Overall ATS score and component breakdown")
    matched_skills: List[str] = Field(default_factory=list, description="List of matched skills")
    missing_skills: List[str] = Field(default_factory=list, description="List of missing skills")
    partial_skills: List[str] = Field(default_factory=list, description="List of partially matched skills")
    match_score: float = Field(..., ge=0.0, le=100.0, description="Overall match score percentage")
    skill_gaps: SkillGapsPrioritySchema = Field(default_factory=SkillGapsPrioritySchema, description="Skill gaps prioritized by level")
    recommendations: List[RecommendationSchema] = Field(default_factory=list, description="Tailored improvement recommendations")
    created_at: datetime = Field(..., description="Timestamp when analysis was created")

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class JobMatchResponse(BaseModel):
    """High-level summary response for job match compatibility."""
    resume_id: str = Field(..., description="Resume ID")
    job_id: str = Field(..., description="Job ID")
    overall_match_percentage: float = Field(..., ge=0.0, le=100.0, description="Overall compatibility percentage")
    key_strengths: List[str] = Field(default_factory=list, description="Top strong matches in candidate profile")
    critical_gaps: List[str] = Field(default_factory=list, description="Most important missing skills or experience")
    summary: str = Field(..., description="Executive summary of job match results")

    model_config = ConfigDict(from_attributes=True)


class SkillGapResponse(BaseModel):
    """Dedicated response schema focusing on skill gap analysis."""
    analysis_id: str = Field(..., description="Analysis ID")
    skill_gaps: SkillGapsPrioritySchema = Field(..., description="Grouped high, medium, and low priority gaps")

    @computed_field
    @property
    def total_gaps_count(self) -> int:
        """Calculates total count of missing skills across high, medium, and low priorities."""
        if not self.skill_gaps:
            return 0
        h = len(self.skill_gaps.high) if self.skill_gaps.high else 0
        m = len(self.skill_gaps.medium) if self.skill_gaps.medium else 0
        l = len(self.skill_gaps.low) if self.skill_gaps.low else 0
        return h + m + l

    model_config = ConfigDict(from_attributes=True)


class RecommendationResponse(BaseModel):
    """Dedicated response schema focusing on recommendations."""
    analysis_id: str = Field(..., description="Analysis ID")
    recommendations: List[RecommendationSchema] = Field(..., description="All actionable recommendations")
    priority_actions: List[str] = Field(default_factory=list, description="Immediate top-priority action items")

    model_config = ConfigDict(from_attributes=True)
