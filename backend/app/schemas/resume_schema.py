"""
Resume schemas for API requests and responses.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class PersonalInfoSchema(BaseModel):
    """Schema for personal contact details."""
    name: str = Field(..., description="Full name of candidate", examples=["Jane Doe"])
    title: Optional[str] = Field(default=None, description="Professional title or headline", examples=["Software Engineer"])
    email: Optional[EmailStr] = Field(default=None, description="Contact email", examples=["jane.doe@example.com"])
    phone: Optional[str] = Field(default=None, description="Contact phone number", examples=["+1 (555) 019-2834"])
    location: Optional[str] = Field(default=None, description="City, State/Country", examples=["San Francisco, CA"])
    linkedin: Optional[str] = Field(default=None, description="LinkedIn profile link", examples=["https://linkedin.com/in/janedoe"])
    github: Optional[str] = Field(default=None, description="GitHub profile link", examples=["https://github.com/janedoe"])
    portfolio: Optional[str] = Field(default=None, description="Portfolio website link", examples=["https://janedoe.dev"])

    model_config = ConfigDict(from_attributes=True)


class EducationItemSchema(BaseModel):
    """Schema for educational qualifications."""
    degree: str = Field(..., description="Degree or diploma name", examples=["B.S. in Computer Science"])
    university: str = Field(..., description="University or college name", examples=["Stanford University"])
    start_date: Optional[str] = Field(default=None, description="Start date", examples=["Sep 2020"])
    end_date: Optional[str] = Field(default=None, description="End date or 'Present'", examples=["May 2024"])
    cgpa: Optional[str] = Field(default=None, description="CGPA or grade", examples=["3.8 / 4.0"])
    coursework: List[str] = Field(default_factory=list, description="Relevant coursework topics", examples=[["Data Structures", "Algorithms", "Database Systems"]])

    model_config = ConfigDict(from_attributes=True)


class SkillsInfoSchema(BaseModel):
    """Schema for categorized technical and soft skills."""
    programming: List[str] = Field(default_factory=list, description="Programming languages", examples=[["Python", "TypeScript", "Go"]])
    frameworks: List[str] = Field(default_factory=list, description="Libraries and frameworks", examples=[["FastAPI", "React", "Next.js"]])
    databases: List[str] = Field(default_factory=list, description="Database systems", examples=[["PostgreSQL", "MongoDB", "Redis"]])
    tools: List[str] = Field(default_factory=list, description="DevOps and developer tools", examples=[["Docker", "Git", "AWS", "Kubernetes"]])
    soft_skills: List[str] = Field(default_factory=list, description="Interpersonal and soft skills", examples=[["Problem Solving", "Team Leadership", "Communication"]])
    other: List[str] = Field(default_factory=list, description="Other specialized skills", examples=[["GraphQL", "REST APIs"]])

    model_config = ConfigDict(from_attributes=True)


class ExperienceItemSchema(BaseModel):
    """Schema for work experience entry."""
    company: str = Field(..., description="Company name", examples=["Acme Corp"])
    position: str = Field(..., description="Job title", examples=["Software Engineering Intern"])
    location: Optional[str] = Field(default=None, description="Job location", examples=["Remote"])
    start_date: Optional[str] = Field(default=None, description="Start date", examples=["Jun 2023"])
    end_date: Optional[str] = Field(default=None, description="End date or 'Present'", examples=["Aug 2023"])
    responsibilities: List[str] = Field(
        default_factory=list,
        description="Key responsibilities",
        examples=[["Developed REST APIs using FastAPI", "Integrated PostgreSQL database with SQLAlchemy"]]
    )
    achievements: List[str] = Field(
        default_factory=list,
        description="Quantifiable accomplishments",
        examples=[["Reduced API response latency by 35% through Redis caching"]]
    )

    model_config = ConfigDict(from_attributes=True)


class ProjectItemSchema(BaseModel):
    """Schema for project entry."""
    name: str = Field(..., description="Project name", examples=["SmartResume AI"])
    description: Optional[str] = Field(default=None, description="Brief project description", examples=["AI-powered ATS Resume Optimizer"])
    technologies: List[str] = Field(default_factory=list, description="Tech stack used", examples=[["Python", "FastAPI", "React", "Pydantic"]])
    github: Optional[str] = Field(default=None, description="GitHub repository URL", examples=["https://github.com/janedoe/smartresume"])
    demo: Optional[str] = Field(default=None, description="Live demo URL", examples=["https://smartresume.example.com"])
    achievements: List[str] = Field(
        default_factory=list,
        description="Project achievements or key metrics",
        examples=[["Achieved 95% test coverage", "Processed over 1,000 resume evaluations"]]
    )

    model_config = ConfigDict(from_attributes=True)


class CertificationItemSchema(BaseModel):
    """Schema for certification entry."""
    name: str = Field(..., description="Certification name", examples=["AWS Certified Solutions Architect"])
    issuer: Optional[str] = Field(default=None, description="Issuing organization", examples=["Amazon Web Services"])
    date: Optional[str] = Field(default=None, description="Issue date", examples=["Jan 2024"])
    url: Optional[str] = Field(default=None, description="Credential URL", examples=["https://aws.amazon.com/verify/12345"])

    model_config = ConfigDict(from_attributes=True)


class LanguageItemSchema(BaseModel):
    """Schema for language proficiency entry."""
    language: str = Field(..., description="Language name", examples=["English"])
    proficiency: Optional[str] = Field(default=None, description="Proficiency level", examples=["Native / Full Professional"])

    model_config = ConfigDict(from_attributes=True)


class VolunteerItemSchema(BaseModel):
    """Schema for volunteer or extracurricular entry."""
    organization: str = Field(..., description="Organization name", examples=["Code for Good"])
    role: str = Field(..., description="Volunteer role or title", examples=["Technical Mentor"])
    start_date: Optional[str] = Field(default=None, description="Start date", examples=["Jan 2023"])
    end_date: Optional[str] = Field(default=None, description="End date", examples=["Dec 2023"])
    description: Optional[str] = Field(default=None, description="Summary of work")
    achievements: List[str] = Field(default_factory=list, description="List of achievements")

    model_config = ConfigDict(from_attributes=True)


class PublicationItemSchema(BaseModel):
    """Schema for research publication entry."""
    title: str = Field(..., description="Paper/Publication title")
    publisher: Optional[str] = Field(default=None, description="Journal or publisher name")
    date: Optional[str] = Field(default=None, description="Publication date")
    url: Optional[str] = Field(default=None, description="Link to publication")
    description: Optional[str] = Field(default=None, description="Brief abstract or summary")

    model_config = ConfigDict(from_attributes=True)


class ReferenceItemSchema(BaseModel):
    """Schema for reference entry."""
    name: str = Field(..., description="Reference full name")
    relationship: Optional[str] = Field(default=None, description="Professional relationship")
    company: Optional[str] = Field(default=None, description="Company/Institution name")
    email: Optional[str] = Field(default=None, description="Contact email")
    phone: Optional[str] = Field(default=None, description="Contact phone")

    model_config = ConfigDict(from_attributes=True)


class ResumeCreate(BaseModel):
    """Payload schema for creating a new resume."""
    title: str = Field(
        default="My Resume",
        min_length=1,
        max_length=150,
        description="Label or title for this resume version"
    )
    personal_info: PersonalInfoSchema = Field(
        ...,
        description="Candidate's personal contact details"
    )
    summary: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Professional summary statement"
    )
    education: List[EducationItemSchema] = Field(
        default_factory=list,
        description="List of education records"
    )
    skills: SkillsInfoSchema = Field(
        default_factory=SkillsInfoSchema,
        description="Categorized technical and soft skills"
    )
    experience: List[ExperienceItemSchema] = Field(
        default_factory=list,
        description="List of work experience entries"
    )
    projects: List[ProjectItemSchema] = Field(
        default_factory=list,
        description="List of projects"
    )
    certifications: List[CertificationItemSchema] = Field(
        default_factory=list,
        description="List of certifications"
    )
    languages: List[LanguageItemSchema] = Field(
        default_factory=list,
        description="List of spoken/written languages"
    )
    achievements: List[str] = Field(
        default_factory=list,
        description="General honors, awards, or achievements"
    )
    volunteer: List[VolunteerItemSchema] = Field(
        default_factory=list,
        description="Volunteer work history"
    )
    publications: List[PublicationItemSchema] = Field(
        default_factory=list,
        description="List of publications"
    )
    references: List[ReferenceItemSchema] = Field(
        default_factory=list,
        description="List of references"
    )
    template: str = Field(
        default="modern",
        description="Design template style identifier"
    )


class ResumeUpdate(BaseModel):
    """Payload schema for updating an existing resume (partial updates allowed)."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=150)
    personal_info: Optional[PersonalInfoSchema] = Field(default=None)
    summary: Optional[str] = Field(default=None, max_length=2000)
    education: Optional[List[EducationItemSchema]] = Field(default=None)
    skills: Optional[SkillsInfoSchema] = Field(default=None)
    experience: Optional[List[ExperienceItemSchema]] = Field(default=None)
    projects: Optional[List[ProjectItemSchema]] = Field(default=None)
    certifications: Optional[List[CertificationItemSchema]] = Field(default=None)
    languages: Optional[List[LanguageItemSchema]] = Field(default=None)
    achievements: Optional[List[str]] = Field(default=None)
    volunteer: Optional[List[VolunteerItemSchema]] = Field(default=None)
    publications: Optional[List[PublicationItemSchema]] = Field(default=None)
    references: Optional[List[ReferenceItemSchema]] = Field(default=None)
    template: Optional[str] = Field(default=None)

    @model_validator(mode="after")
    def check_at_least_one_field(self) -> "ResumeUpdate":
        """Verify that at least one field is supplied for update."""
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided to update resume.")
        return self


class ResumeResponse(BaseModel):
    """Response schema representing a complete resume."""
    resume_id: str = Field(..., description="Unique resume identifier")
    user_id: str = Field(..., description="Owner user ID")
    title: str = Field(..., description="Resume title label")
    personal_info: PersonalInfoSchema = Field(..., description="Personal info details")
    summary: Optional[str] = Field(default=None, description="Professional summary")
    education: List[EducationItemSchema] = Field(default_factory=list)
    skills: SkillsInfoSchema = Field(default_factory=SkillsInfoSchema)
    experience: List[ExperienceItemSchema] = Field(default_factory=list)
    projects: List[ProjectItemSchema] = Field(default_factory=list)
    certifications: List[CertificationItemSchema] = Field(default_factory=list)
    languages: List[LanguageItemSchema] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    volunteer: List[VolunteerItemSchema] = Field(default_factory=list)
    publications: List[PublicationItemSchema] = Field(default_factory=list)
    references: List[ReferenceItemSchema] = Field(default_factory=list)
    template: str = Field(default="modern", description="Template identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last updated timestamp")

    model_config = ConfigDict(from_attributes=True)
