"""
Job model for SmartResume AI.
"""

from datetime import datetime
from typing import List, Optional
import uuid

from pydantic import BaseModel, ConfigDict, Field


class ExtractedSkills(BaseModel):
    """Extracted required and preferred skills from job description."""
    required: List[str] = Field(
        default_factory=list,
        description="Mandatory skills required for the role"
    )
    preferred: List[str] = Field(
        default_factory=list,
        description="Optional or nice-to-have skills"
    )

    model_config = ConfigDict(from_attributes=True)


class Job(BaseModel):
    """
    Job domain and database model.
    """
    job_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the job posting"
    )
    user_id: str = Field(
        ...,
        description="ID of the user who saved or imported this job posting"
    )
    job_title: str = Field(
        ...,
        description="Title of the target job position"
    )
    job_description: str = Field(
        ...,
        description="Full text of the job description"
    )
    extracted_skills: ExtractedSkills = Field(
        default_factory=ExtractedSkills,
        description="Extracted required and preferred skills"
    )
    keywords: List[str] = Field(
        default_factory=list,
        description="Keywords and core phrases extracted from the job description"
    )
    experience_required: Optional[str] = Field(
        default=None,
        description="Experience level or years of experience required"
    )
    education_required: Optional[str] = Field(
        default=None,
        description="Minimum education or degree required"
    )
    company_name: Optional[str] = Field(
        default=None,
        description="Name of hiring company (optional)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the job entry was created"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "job_id": "c3d4e5f6-7890-abcd-ef01-234567890abc",
                "user_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
                "job_title": "Senior Frontend Engineer",
                "job_description": "Looking for a React developer with 5+ years experience...",
                "extracted_skills": {
                    "required": ["React", "TypeScript", "JavaScript", "HTML/CSS"],
                    "preferred": ["Next.js", "GraphQL", "TailwindCSS"]
                },
                "keywords": ["React", "Frontend", "UI/UX", "State Management"],
                "experience_required": "5+ years",
                "education_required": "Bachelor's in Computer Science or equivalent",
                "company_name": "TechCorp",
                "created_at": "2026-08-22T12:00:00Z"
            }
        }
    )
