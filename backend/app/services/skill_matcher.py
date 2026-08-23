"""
Skill Matching & Gap Analysis Engine for SmartResume AI.

Normalizes skills across aliases, matches candidate resume skills against job requirements,
and calculates comprehensive skill gap analysis categorized by priority.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set, Union, Any
from difflib import SequenceMatcher
import re


SKILL_ALIASES: Dict[str, str] = {
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "py": "Python",
    "python": "Python",
    "py3": "Python",
    "react": "React",
    "react.js": "React",
    "reactjs": "React",
    "vue": "Vue.js",
    "vue.js": "Vue.js",
    "vuejs": "Vue.js",
    "node": "Node.js",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "next": "Next.js",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "express": "Express.js",
    "express.js": "Express.js",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "docker": "Docker",
    "aws": "AWS",
    "amazon web services": "AWS",
    "gcp": "Google Cloud",
    "google cloud platform": "Google Cloud",
    "google cloud": "Google Cloud",
    "azure": "Azure",
    "microsoft azure": "Azure",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "fastapi": "FastAPI",
    "django": "Django",
    "flask": "Flask",
    "spring": "Spring Boot",
    "springboot": "Spring Boot",
    "spring boot": "Spring Boot",
    "cpp": "C++",
    "c++": "C++",
    "csharp": "C#",
    "c#": "C#",
    "net": ".NET",
    ".net": ".NET",
    "dotnet": ".NET",
    "rest": "REST API",
    "restful": "REST API",
    "rest api": "REST API",
    "restful api": "REST API",
    "graphql": "GraphQL",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "git": "Git",
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",
    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch"
}


@dataclass
class MatchResult:
    """Represents overall skill matching results between CV and Job."""
    match_percentage: float
    matched_skills: List[str] = field(default_factory=list)
    partial_matches: List[Dict[str, str]] = field(default_factory=list)  # {"job_skill": ..., "resume_skill": ...}
    missing_skills: List[str] = field(default_factory=list)
    total_job_skills: int = 0
    total_resume_skills: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert MatchResult to dictionary."""
        return asdict(self)


@dataclass
class SkillGap:
    """Represents a single identified skill gap."""
    skill_name: str
    priority: str  # HIGH, MEDIUM, LOW
    category: str  # e.g., "required_core", "required_secondary", "preferred"
    reason: str


@dataclass
class SkillGapResult:
    """Represents priority-classified skill gap analysis."""
    high_priority_gaps: List[str] = field(default_factory=list)
    medium_priority_gaps: List[str] = field(default_factory=list)
    low_priority_gaps: List[str] = field(default_factory=list)
    gap_details: List[Dict[str, Any]] = field(default_factory=list)
    total_gaps: int = 0
    match_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert SkillGapResult to dictionary."""
        return asdict(self)


class SkillMatcher:
    """Engine for normalizing, matching, and scoring skills between resumes and jobs."""

    def __init__(self, aliases: Optional[Dict[str, str]] = None):
        """Initialize SkillMatcher with alias map."""
        self.aliases = aliases or SKILL_ALIASES

    def normalize_skill(self, skill_name: str) -> str:
        """
        Normalize skill name (lowercase, strip, map alias).

        Args:
            skill_name: Raw skill string (e.g., ' JS ', 'react.js').

        Returns:
            Standardized canonical skill string (e.g., 'JavaScript', 'React').
        """
        if not skill_name or not isinstance(skill_name, str):
            return ""

        cleaned = skill_name.strip().lower()
        # Direct lookup in alias dictionary
        if cleaned in self.aliases:
            return self.aliases[cleaned]

        # Strip special trailing chars like .js or .py
        sub_cleaned = re.sub(r'[\.\-\_]', '', cleaned)
        if sub_cleaned in self.aliases:
            return self.aliases[sub_cleaned]

        # Return title-cased or uppercase format for standard strings
        if len(cleaned) <= 3 and cleaned.isalnum():
            return cleaned.upper()
        return skill_name.strip().title()

    def match_resume_to_job(
        self,
        resume_skills: Union[List[str], Set[str]],
        job_skills: Union[List[str], Set[str]]
    ) -> MatchResult:
        """
        Match resume skills against target job skills.

        Args:
            resume_skills: List/set of candidate's skills.
            job_skills: List/set of job requirement skills.

        Returns:
            MatchResult containing matched, partial, missing skills & score percentage.
        """
        resume_list = list(resume_skills) if resume_skills else []
        job_list = list(job_skills) if job_skills else []

        # Normalize skills lists
        norm_resume_map: Dict[str, str] = {self.normalize_skill(s): s for s in resume_list if s}
        norm_job_map: Dict[str, str] = {self.normalize_skill(s): s for s in job_list if s}

        norm_resume_set = set(norm_resume_map.keys())
        norm_job_set = set(norm_job_map.keys())

        matched_skills: List[str] = []
        partial_matches: List[Dict[str, str]] = []
        missing_skills: List[str] = []

        unmatched_job_skills = set(norm_job_set)

        # 1. Exact canonical matches
        for norm_j in list(unmatched_job_skills):
            if norm_j in norm_resume_set:
                matched_skills.append(norm_j)
                unmatched_job_skills.remove(norm_j)

        # 2. Partial / Fuzzy / Substring matches for remaining job skills
        unmatched_resume_skills = norm_resume_set - set(matched_skills)

        for norm_j in list(unmatched_job_skills):
            found_partial = False
            for norm_r in unmatched_resume_skills:
                # Fuzzy ratio check or substring containment
                similarity = SequenceMatcher(None, norm_j.lower(), norm_r.lower()).ratio()
                is_substring = (len(norm_j) > 3 and norm_j.lower() in norm_r.lower()) or \
                               (len(norm_r) > 3 and norm_r.lower() in norm_j.lower())

                if similarity >= 0.82 or is_substring:
                    partial_matches.append({
                        "job_skill": norm_j,
                        "resume_skill": norm_r,
                        "similarity": round(similarity, 2)
                    })
                    found_partial = True
                    break

            if not found_partial:
                missing_skills.append(norm_j)

        # Calculate percentage match score
        total_job = len(norm_job_set)
        if total_job == 0:
            match_score = 100.0
        else:
            # Full credit (1.0) for exact match, half credit (0.5) for partial match
            raw_score = (len(matched_skills) * 1.0 + len(partial_matches) * 0.5) / total_job * 100.0
            match_score = round(min(100.0, max(0.0, raw_score)), 1)

        return MatchResult(
            match_percentage=match_score,
            matched_skills=sorted(matched_skills),
            partial_matches=partial_matches,
            missing_skills=sorted(missing_skills),
            total_job_skills=total_job,
            total_resume_skills=len(norm_resume_set)
        )

    def analyze_skill_gap(
        self,
        resume_skills: List[str],
        job_required: List[str],
        job_preferred: Optional[List[str]] = None
    ) -> SkillGapResult:
        """
        Classify missing skills into HIGH, MEDIUM, and LOW priority gaps.

        - HIGH Priority: Required core technical skills (languages, main frameworks, databases)
        - MEDIUM Priority: Required secondary skills (tools, soft skills, methodologies)
        - LOW Priority: Preferred or nice-to-have skills
        """
        job_preferred = job_preferred or []

        # Run matchers
        match_req = self.match_resume_to_job(resume_skills, job_required)
        match_pref = self.match_resume_to_job(resume_skills, job_preferred)

        # Identify core vs secondary skill categories
        core_keywords = {'python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'go', 'rust',
                         'react', 'angular', 'vue', 'django', 'fastapi', 'node.js', 'spring boot',
                         'postgresql', 'mysql', 'mongodb', 'aws', 'docker', 'kubernetes'}

        high_priority: List[str] = []
        medium_priority: List[str] = []
        low_priority: List[str] = []
        gap_details: List[Dict[str, Any]] = []

        # Process missing required skills
        for skill in match_req.missing_skills:
            norm_skill = skill.lower()
            if norm_skill in core_keywords or any(ck in norm_skill for ck in core_keywords):
                priority = "HIGH"
                category = "required_core"
                reason = f"Essential required core skill for the position."
                high_priority.append(skill)
            else:
                priority = "MEDIUM"
                category = "required_secondary"
                reason = f"Required tool, methodology, or supporting skill."
                medium_priority.append(skill)

            gap_details.append({
                "skill": skill,
                "priority": priority,
                "category": category,
                "reason": reason
            })

        # Process missing preferred skills
        for skill in match_pref.missing_skills:
            if skill not in match_req.matched_skills and skill not in match_req.missing_skills:
                priority = "LOW"
                category = "preferred"
                reason = "Nice-to-have bonus skill."
                low_priority.append(skill)
                gap_details.append({
                    "skill": skill,
                    "priority": priority,
                    "category": category,
                    "reason": reason
                })

        total_gaps = len(high_priority) + len(medium_priority) + len(low_priority)

        return SkillGapResult(
            high_priority_gaps=sorted(high_priority),
            medium_priority_gaps=sorted(medium_priority),
            low_priority_gaps=sorted(low_priority),
            gap_details=gap_details,
            total_gaps=total_gaps,
            match_score=match_req.match_percentage
        )


def match_resume_to_job(resume_skills: List[str], job_skills: List[str]) -> MatchResult:
    """Convenience function to match resume skills against job skills."""
    matcher = SkillMatcher()
    return matcher.match_resume_to_job(resume_skills, job_skills)


def analyze_skill_gap(
    resume_skills: List[str],
    job_required: List[str],
    job_preferred: Optional[List[str]] = None
) -> SkillGapResult:
    """Convenience function to analyze skill gaps by priority."""
    matcher = SkillMatcher()
    return matcher.analyze_skill_gap(resume_skills, job_required, job_preferred)
