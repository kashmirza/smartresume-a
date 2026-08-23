"""
Resume model for SmartResume AI.
"""

from datetime import datetime
from typing import List, Optional
import uuid

from pydantic import BaseModel, ConfigDict, Field


class PersonalInfo(BaseModel):
    """Personal contact and identification details."""
    name: str = Field(..., description="Full candidate name")
    title: Optional[str] = Field(default=None, description="Professional headline or title")
    email: Optional[str] = Field(default=None, description="Contact email address")
    phone: Optional[str] = Field(default=None, description="Contact phone number")
    location: Optional[str] = Field(default=None, description="City, State/Country")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn profile URL")
    github: Optional[str] = Field(default=None, description="GitHub profile URL")
    portfolio: Optional[str] = Field(default=None, description="Personal website or portfolio URL")

    model_config = ConfigDict(from_attributes=True)


class EducationItem(BaseModel):
    """Educational background entry."""
    degree: str = Field(..., description="Degree or certificate title")
    university: str = Field(..., description="University or educational institution name")
    start_date: Optional[str] = Field(default=None, description="Start date (e.g., 'Sep 2020')")
    end_date: Optional[str] = Field(default=None, description="End date or 'Present'")
    cgpa: Optional[str] = Field(default=None, description="CGPA or Grade")
    coursework: List[str] = Field(default_factory=list, description="List of relevant coursework subjects")

    model_config = ConfigDict(from_attributes=True)


class SkillsInfo(BaseModel):
    """Categorized technical and soft skills."""
    programming: List[str] = Field(default_factory=list, description="Programming languages")
    frameworks: List[str] = Field(default_factory=list, description="Libraries and frameworks")
    databases: List[str] = Field(default_factory=list, description="Database systems")
    tools: List[str] = Field(default_factory=list, description="Tools, platforms, and DevOps")
    soft_skills: List[str] = Field(default_factory=list, description="Soft skills and personal attributes")
    other: List[str] = Field(default_factory=list, description="Additional skills and domains")

    model_config = ConfigDict(from_attributes=True)


class ExperienceItem(BaseModel):
    """Work experience entry."""
    company: str = Field(..., description="Company or organization name")
    position: str = Field(..., description="Job title or role")
    location: Optional[str] = Field(default=None, description="Job location")
    start_date: Optional[str] = Field(default=None, description="Start date")
    end_date: Optional[str] = Field(default=None, description="End date or 'Present'")
    responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities and tasks")
    achievements: List[str] = Field(default_factory=list, description="Quantifiable achievements and impact")

    model_config = ConfigDict(from_attributes=True)


class ProjectItem(BaseModel):
    """Project entry."""
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(default=None, description="Overview of the project")
    technologies: List[str] = Field(default_factory=list, description="Tech stack and tools used")
    github: Optional[str] = Field(default=None, description="Repository link")
    demo: Optional[str] = Field(default=None, description="Live demo or deployment link")
    achievements: List[str] = Field(default_factory=list, description="Key features or achievements")

    model_config = ConfigDict(from_attributes=True)


class CertificationItem(BaseModel):
    """Professional certification entry."""
    name: str = Field(..., description="Certification title")
    issuer: Optional[str] = Field(default=None, description="Issuing body or organization")
    date: Optional[str] = Field(default=None, description="Issue date")
    url: Optional[str] = Field(default=None, description="Verification or credential URL")

    model_config = ConfigDict(from_attributes=True)


class LanguageItem(BaseModel):
    """Spoken or written language proficiency."""
    language: str = Field(..., description="Language name")
    proficiency: Optional[str] = Field(default=None, description="Proficiency level (e.g. Native, Fluent, Intermediate)")

    model_config = ConfigDict(from_attributes=True)


class VolunteerItem(BaseModel):
    """Volunteer work or community experience entry."""
    organization: str = Field(..., description="Organization name")
    role: str = Field(..., description="Volunteer position or title")
    start_date: Optional[str] = Field(default=None, description="Start date")
    end_date: Optional[str] = Field(default=None, description="End date or 'Present'")
    description: Optional[str] = Field(default=None, description="Summary of activities")
    achievements: List[str] = Field(default_factory=list, description="Impact or achievements")

    model_config = ConfigDict(from_attributes=True)


class PublicationItem(BaseModel):
    """Research paper or publication entry."""
    title: str = Field(..., description="Publication title")
    publisher: Optional[str] = Field(default=None, description="Publisher, journal, or conference")
    date: Optional[str] = Field(default=None, description="Publication date")
    url: Optional[str] = Field(default=None, description="Link to publication")
    description: Optional[str] = Field(default=None, description="Abstract or summary")

    model_config = ConfigDict(from_attributes=True)


class ReferenceItem(BaseModel):
    """Professional reference entry."""
    name: str = Field(..., description="Reference person name")
    relationship: Optional[str] = Field(default=None, description="Professional relationship")
    company: Optional[str] = Field(default=None, description="Company or institution")
    email: Optional[str] = Field(default=None, description="Contact email")
    phone: Optional[str] = Field(default=None, description="Contact phone")

    model_config = ConfigDict(from_attributes=True)


class Resume(BaseModel):
    """
    Resume domain and database model.
    """
    resume_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the resume"
    )
    user_id: str = Field(
        ...,
        description="User ID of the resume owner"
    )
    title: str = Field(
        default="My Resume",
        description="User label or title for this resume version"
    )
    personal_info: PersonalInfo = Field(
        ...,
        description="Personal contact and header information"
    )
    summary: Optional[str] = Field(
        default=None,
        description="Professional summary or objective statement"
    )
    education: List[EducationItem] = Field(
        default_factory=list,
        description="Educational history"
    )
    skills: SkillsInfo = Field(
        default_factory=SkillsInfo,
        description="Categorized technical and soft skills"
    )
    experience: List[ExperienceItem] = Field(
        default_factory=list,
        description="Work experience entries"
    )
    projects: List[ProjectItem] = Field(
        default_factory=list,
        description="Key projects"
    )
    certifications: List[CertificationItem] = Field(
        default_factory=list,
        description="Certifications and courses"
    )
    languages: List[LanguageItem] = Field(
        default_factory=list,
        description="Languages spoken"
    )
    achievements: List[str] = Field(
        default_factory=list,
        description="Honors, awards, and general achievements"
    )
    volunteer: List[VolunteerItem] = Field(
        default_factory=list,
        description="Volunteer and extracurricular experience"
    )
    publications: List[PublicationItem] = Field(
        default_factory=list,
        description="Research papers, articles, or books"
    )
    references: List[ReferenceItem] = Field(
        default_factory=list,
        description="Professional references"
    )
    template: str = Field(
        default="modern",
        description="Design/formatting template style (e.g. 'modern', 'classic', 'minimal')"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when resume was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when resume was last updated"
    )

    model_config = ConfigDict(from_attributes=True)
