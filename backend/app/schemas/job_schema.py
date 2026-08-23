"""
Job schemas for API requests and responses.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field


class ExtractedSkillsSchema(BaseModel):
    """Schema for extracted required and preferred job skills."""
    required: List[str] = Field(
        default_factory=list,
        description="Mandatory skills extracted from job description",
        examples=[["Python", "FastAPI", "SQL"]]
    )
    preferred: List[str] = Field(
        default_factory=list,
        description="Optional or preferred skills",
        examples=[["Docker", "AWS", "Redis"]]
    )

    model_config = ConfigDict(from_attributes=True)


class JobCreate(BaseModel):
    """Payload schema for creating/posting a job entry for ATS evaluation."""
    job_title: str = Field(
        ...,
        min_length=2,
        max_length=150,
        description="Target position title",
        examples=["Backend Engineer"]
    )
    job_description: str = Field(
        ...,
        min_length=10,
        description="Full job description text",
        examples=["We are seeking a Backend Engineer skilled in Python and REST APIs..."]
    )
    extracted_skills: Optional[ExtractedSkillsSchema] = Field(
        default=None,
        description="Pre-extracted skills (if auto-extraction is bypassed)"
    )
    keywords: List[str] = Field(
        default_factory=list,
        description="Key phrases and industry terms",
        examples=[["Python", "Microservices", "REST API"]]
    )
    experience_required: Optional[str] = Field(
        default=None,
        description="Required experience level or years",
        examples=["3+ years"]
    )
    education_required: Optional[str] = Field(
        default=None,
        description="Required educational degree",
        examples=["Bachelor's degree in CS or related field"]
    )
    company_name: Optional[str] = Field(
        default=None,
        description="Hiring company name",
        examples=["Tech Corp"]
    )


class JobResponse(BaseModel):
    """Response schema representing a stored job entry."""
    job_id: str = Field(..., description="Unique job posting ID")
    user_id: str = Field(..., description="ID of user who created the entry")
    job_title: str = Field(..., description="Job title")
    job_description: str = Field(..., description="Full job description text")
    extracted_skills: ExtractedSkillsSchema = Field(..., description="Extracted required & preferred skills")
    keywords: List[str] = Field(default_factory=list, description="Extracted keywords")
    experience_required: Optional[str] = Field(default=None, description="Experience requirements")
    education_required: Optional[str] = Field(default=None, description="Education requirements")
    company_name: Optional[str] = Field(default=None, description="Company name")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class JobAnalysisResponse(BaseModel):
    """Summary response schema after parsing/analyzing a job description."""
    job_id: str = Field(..., description="Unique job ID")
    job_title: str = Field(..., description="Job position title")
    company_name: Optional[str] = Field(default=None, description="Company name")
    extracted_skills: ExtractedSkillsSchema = Field(..., description="Extracted required & preferred skills")
    keywords: List[str] = Field(default_factory=list, description="Top extracted keywords")
    experience_required: Optional[str] = Field(default=None, description="Extracted experience requirement")
    education_required: Optional[str] = Field(default=None, description="Extracted education requirement")
    summary: Optional[str] = Field(default=None, description="Brief AI-generated summary of the job post")
    created_at: datetime = Field(..., description="Creation timestamp")

    @computed_field
    @property
    def total_skills_count(self) -> int:
        """Calculates total count of required and preferred skills."""
        if not self.extracted_skills:
            return 0
        req = len(self.extracted_skills.required) if self.extracted_skills.required else 0
        pref = len(self.extracted_skills.preferred) if self.extracted_skills.preferred else 0
        return req + pref

    model_config = ConfigDict(from_attributes=True)
