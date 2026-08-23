from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class PersonalInfo(BaseModel):
    full_name: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""
    location: Optional[str] = ""
    linkedin_url: Optional[str] = ""
    github_url: Optional[str] = ""
    website_url: Optional[str] = ""


class ExperienceItem(BaseModel):
    company_name: Optional[str] = ""
    position_title: Optional[str] = ""
    start_date: Optional[str] = ""
    end_date: Optional[str] = ""
    location: Optional[str] = ""
    description: Optional[str] = ""
    bullet_points: List[str] = Field(default_factory=list)


class EducationItem(BaseModel):
    institution: Optional[str] = ""
    degree: Optional[str] = ""
    field_of_study: Optional[str] = ""
    start_date: Optional[str] = ""
    end_date: Optional[str] = ""
    gpa: Optional[str] = ""


class ProjectItem(BaseModel):
    title: Optional[str] = ""
    description: Optional[str] = ""
    technologies: List[str] = Field(default_factory=list)
    date: Optional[str] = ""
    link: Optional[str] = ""


class ResumeCreate(BaseModel):
    title: str = Field(..., example="Senior Software Engineer Resume")
    target_role: Optional[str] = "Software Engineer"
    personal_info: Optional[Dict[str, Any]] = Field(default_factory=dict)
    summary: Optional[str] = ""
    work_experience: List[Dict[str, Any]] = Field(default_factory=list)
    education: List[Dict[str, Any]] = Field(default_factory=list)
    skills: List[Any] = Field(default_factory=list)
    projects: List[Dict[str, Any]] = Field(default_factory=list)
    certifications: List[Any] = Field(default_factory=list)
    languages: List[Any] = Field(default_factory=list)
    template_id: Optional[str] = "ats_classic"


class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    target_role: Optional[str] = None
    personal_info: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    work_experience: Optional[List[Dict[str, Any]]] = None
    education: Optional[List[Dict[str, Any]]] = None
    skills: Optional[List[Any]] = None
    projects: Optional[List[Dict[str, Any]]] = None
    certifications: Optional[List[Any]] = None
    languages: Optional[List[Any]] = None
    template_id: Optional[str] = None


class AtsAnalysisRequest(BaseModel):
    job_description: Optional[str] = None
    target_role: Optional[str] = None
    job_id: Optional[str] = None


class ResumeOptimizeRequest(BaseModel):
    job_description: Optional[str] = None
    target_role: Optional[str] = None
    sections: Optional[List[str]] = None
