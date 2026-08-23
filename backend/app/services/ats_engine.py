"""
ATS Scoring & Resume Analysis Engine for SmartResume AI.

Evaluates resumes across Keyword Match (30%), Section Completeness (20%),
Formatting (15%), Skills Relevance (15%), Experience Relevance (10%),
and Content Quality (10%) to produce an overall ATS score and actionable insights.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Union
import re

from app.services.job_parser import JobParser, SKILLS_DATABASE
from app.services.skill_matcher import SkillMatcher
from app.services.resume_optimizer import ACHIEVEMENT_VERBS, WEAK_PHRASES_MAP


REQUIRED_SECTIONS = [
    "contact",
    "summary",
    "skills",
    "experience",
    "education",
    "projects",
    "certifications"
]

STANDARD_SECTION_NAMES = {
    "contact": ["contact", "contact_info", "personal_info", "contact information"],
    "summary": ["summary", "professional_summary", "about", "objective", "profile"],
    "skills": ["skills", "technical_skills", "core_competencies", "skills & expertise"],
    "experience": ["experience", "work_experience", "employment", "professional_experience", "work history"],
    "education": ["education", "academic_background", "academic_history", "education & training"],
    "projects": ["projects", "key_projects", "personal_projects", "selected_projects"],
    "certifications": ["certifications", "certificates", "licenses", "certifications & licenses"]
}


@dataclass
class ATSAnalysisResult:
    """Comprehensive ATS Resume Evaluation Result."""
    overall_score: float
    grade: str
    score_breakdown: Dict[str, float]  # Percentage contribution for each category
    sub_scores: Dict[str, float]       # Raw 0-100 scores for each category
    sections_analysis: Dict[str, Any]
    formatting_analysis: Dict[str, Any]
    keyword_analysis: Dict[str, Any]
    skills_relevance_analysis: Dict[str, Any]
    experience_relevance_analysis: Dict[str, Any]
    content_quality_analysis: Dict[str, Any]
    suggestions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert ATSAnalysisResult to dictionary."""
        return asdict(self)


class ATSEngine:
    """Production ATS Analysis and Scoring Engine."""

    # Category Weights summing to 1.0 (100%)
    WEIGHTS = {
        "keyword_match": 0.30,
        "section_completeness": 0.20,
        "formatting": 0.15,
        "skills_relevance": 0.15,
        "experience_relevance": 0.10,
        "content_quality": 0.10
    }

    def __init__(self):
        """Initialize ATS Engine with supporting sub-parsers."""
        self.job_parser = JobParser()
        self.skill_matcher = SkillMatcher()

    def analyze_resume(
        self,
        resume_data: Union[Dict[str, Any], Any],
        job_data: Optional[Union[Dict[str, Any], str, Any]] = None
    ) -> ATSAnalysisResult:
        """
        Perform complete ATS evaluation on resume_data against optional job_data.

        Args:
            resume_data: Dict or model representing structured resume.
            job_data: Optional job description text, dict, or JobAnalysis object.

        Returns:
            ATSAnalysisResult containing overall score, breakdown, sub-scores, and recommendations.
        """
        data = self._to_dict(resume_data)

        # Process job_data if provided as text or dict
        parsed_job = None
        if isinstance(job_data, str) and job_data.strip():
            parsed_job = self.job_parser.parse_job_description(job_data)
        elif isinstance(job_data, dict):
            parsed_job = job_data
        elif hasattr(job_data, "to_dict"):
            parsed_job = job_data.to_dict()

        # Run 6 sub-evaluations
        sections_res = self.check_sections(data)
        formatting_res = self.check_formatting(data)
        keyword_res = self.analyze_keywords(data, parsed_job)
        skills_rel_res = self.analyze_skills_relevance(data, parsed_job)
        exp_rel_res = self.analyze_experience_relevance(data, parsed_job)
        quality_res = self.analyze_content_quality(data)

        # Extract 0-100 sub-scores
        sub_scores = {
            "keyword_match": keyword_res.get("score", 70.0),
            "section_completeness": sections_res.get("score", 0.0),
            "formatting": formatting_res.get("score", 100.0),
            "skills_relevance": skills_rel_res.get("score", 70.0),
            "experience_relevance": exp_rel_res.get("score", 70.0),
            "content_quality": quality_res.get("score", 70.0)
        }

        # Calculate weighted score breakdown and overall score
        score_breakdown: Dict[str, float] = {}
        overall_score = 0.0

        for key, weight in self.WEIGHTS.items():
            weighted_val = round(sub_scores[key] * weight, 2)
            score_breakdown[key] = weighted_val
            overall_score += weighted_val

        overall_score = round(min(100.0, max(0.0, overall_score)), 1)
        grade = self._calculate_grade(overall_score)

        # Aggregate suggestions across modules
        suggestions = self._collect_suggestions(
            sections_res, formatting_res, keyword_res, skills_rel_res, exp_rel_res, quality_res
        )

        return ATSAnalysisResult(
            overall_score=overall_score,
            grade=grade,
            score_breakdown=score_breakdown,
            sub_scores=sub_scores,
            sections_analysis=sections_res,
            formatting_analysis=formatting_res,
            keyword_analysis=keyword_res,
            skills_relevance_analysis=skills_rel_res,
            experience_relevance_analysis=exp_rel_res,
            content_quality_analysis=quality_res,
            suggestions=suggestions
        )

    def check_sections(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify presence of mandatory and optional ATS sections.

        Required: contact, summary, skills, experience, education, projects, certifications.
        """
        present_sections: List[str] = []
        missing_sections: List[str] = []
        section_details: Dict[str, bool] = {}

        for sec in REQUIRED_SECTIONS:
            found = False
            # Check primary key and alias variations
            aliases = STANDARD_SECTION_NAMES.get(sec, [sec])
            for alias in aliases:
                val = resume_data.get(alias)
                if val is not None and (bool(val) or len(str(val).strip()) > 0):
                    found = True
                    break

            section_details[sec] = found
            if found:
                present_sections.append(sec)
            else:
                missing_sections.append(sec)

        # Core vs optional section weighting
        # Mandatory: contact, skills, experience, education (80% weight)
        # Recommended: summary, projects, certifications (20% weight)
        mandatory = ["contact", "skills", "experience", "education"]
        recommended = ["summary", "projects", "certifications"]

        mand_present = sum(1 for m in mandatory if section_details.get(m))
        rec_present = sum(1 for r in recommended if section_details.get(r))

        score = (mand_present / len(mandatory) * 80.0) + (rec_present / len(recommended) * 20.0)
        score = round(min(100.0, max(0.0, score)), 1)

        return {
            "score": score,
            "present_sections": present_sections,
            "missing_sections": missing_sections,
            "section_details": section_details,
            "total_present": len(present_sections),
            "total_required": len(REQUIRED_SECTIONS)
        }

    def check_formatting(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate ATS-friendly formatting rules:
        - No tables or complex non-linear columns
        - Standard section headers
        - Appropriate text length & bullet formatting
        """
        score = 100.0
        issues: List[str] = []
        checks = {
            "no_tables": True,
            "standard_section_names": True,
            "simple_layout": True,
            "no_graphics_flags": True,
            "appropriate_length": True
        }

        # Check for table or column flags if present in data
        if resume_data.get("contains_tables") or resume_data.get("has_tables"):
            checks["no_tables"] = False
            issues.append("Resume contains tables which can confuse ATS parsers.")
            score -= 20.0

        if resume_data.get("contains_graphics") or resume_data.get("has_images"):
            checks["no_graphics_flags"] = False
            issues.append("Graphics, images, or chart elements detected. Use text only for ATS compatibility.")
            score -= 15.0

        # Check section names against standard vocabulary
        unstandardized_headers = []
        for key in resume_data.keys():
            if key in ["contains_tables", "contains_graphics", "raw_text", "formatting_flags"]:
                continue
            is_std = any(key in aliases for aliases in STANDARD_SECTION_NAMES.values())
            if not is_std and len(key) < 30:
                unstandardized_headers.append(key)

        if len(unstandardized_headers) > 2:
            checks["standard_section_names"] = False
            issues.append(f"Non-standard section header names detected: {', '.join(unstandardized_headers[:3])}.")
            score -= 10.0

        # Check total word count appropriateness (300 to 1200 words is standard)
        text_content = self._extract_all_text(resume_data)
        word_count = len(text_content.split())
        if word_count > 0 and (word_count < 150 or word_count > 1500):
            checks["appropriate_length"] = False
            issues.append(f"Resume length ({word_count} words) is outside ideal ATS range (250-1200 words).")
            score -= 10.0

        score = round(min(100.0, max(0.0, score)), 1)

        return {
            "score": score,
            "checks": checks,
            "issues": issues,
            "word_count": word_count,
            "is_ats_friendly": score >= 80.0
        }

    def analyze_keywords(
        self,
        resume_data: Dict[str, Any],
        job_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Extract job description keywords and calculate keyword match density against resume.
        """
        resume_text = self._extract_all_text(resume_data).lower()

        if not job_data:
            # Fallback when no job description is provided: evaluate presence of industry tech terms
            tech_found = []
            for cat_skills in SKILLS_DATABASE.values():
                for skill in cat_skills:
                    if re.search(r'\b' + re.escape(skill.lower()) + r'\b', resume_text):
                        tech_found.append(skill)

            unique_tech = list(dict.fromkeys(tech_found))
            score = min(100.0, len(unique_tech) * 5.0) if unique_tech else 50.0

            return {
                "score": round(score, 1),
                "matched_keywords": unique_tech[:15],
                "missing_keywords": [],
                "keyword_density": round(len(unique_tech) / max(1, len(resume_text.split())) * 100, 2),
                "note": "No job description provided; scored based on general technical keyword presence."
            }

        # Job data is present: extract keywords from job_data
        job_keywords = []
        if isinstance(job_data, dict):
            job_keywords = job_data.get("keywords", []) or job_data.get("required_skills", [])
            if not job_keywords and "raw_text" in job_data:
                parsed = self.job_parser.parse_job_description(job_data["raw_text"])
                job_keywords = parsed.keywords

        matched: List[str] = []
        missing: List[str] = []

        for kw in job_keywords:
            pattern = r'(?:\b|_)' + re.escape(kw.lower()) + r'(?:\b|_)'
            if re.search(pattern, resume_text):
                matched.append(kw)
            else:
                missing.append(kw)

        total_kw = len(job_keywords)
        score = (len(matched) / total_kw * 100.0) if total_kw > 0 else 80.0
        score = round(min(100.0, max(0.0, score)), 1)

        return {
            "score": score,
            "matched_keywords": sorted(matched),
            "missing_keywords": sorted(missing),
            "matched_count": len(matched),
            "total_job_keywords": total_kw
        }

    def analyze_skills_relevance(
        self,
        resume_data: Dict[str, Any],
        job_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Evaluate alignment of candidate's skills with job requirements."""
        resume_skills = self._extract_skills_list(resume_data)

        if not job_data:
            score = 80.0 if len(resume_skills) >= 5 else (len(resume_skills) * 15.0)
            return {
                "score": round(min(100.0, score), 1),
                "skills_count": len(resume_skills),
                "matched_skills": resume_skills,
                "missing_skills": []
            }

        required_skills = job_data.get("required_skills", [])
        match_result = self.skill_matcher.match_resume_to_job(resume_skills, required_skills)

        return {
            "score": match_result.match_percentage,
            "matched_skills": match_result.matched_skills,
            "partial_matches": match_result.partial_matches,
            "missing_skills": match_result.missing_skills,
            "total_resume_skills": match_result.total_resume_skills,
            "total_job_skills": match_result.total_job_skills
        }

    def analyze_experience_relevance(
        self,
        resume_data: Dict[str, Any],
        job_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Evaluate work experience depth, tenure, and relevance."""
        experience = resume_data.get("experience", []) or resume_data.get("work_experience", [])
        
        if not experience:
            return {
                "score": 0.0,
                "experience_entries_count": 0,
                "notes": "No work experience entries found."
            }

        entries_count = len(experience)
        bullet_count = 0
        has_dates = False

        for exp in experience:
            if isinstance(exp, dict):
                bullets = exp.get("highlights", []) or exp.get("description", []) or exp.get("bullets", [])
                if isinstance(bullets, list):
                    bullet_count += len(bullets)
                elif isinstance(bullets, str) and bullets.strip():
                    bullet_count += 1
                if exp.get("dates") or exp.get("start_date"):
                    has_dates = True

        score = 60.0
        if entries_count >= 2:
            score += 20.0
        if bullet_count >= 4:
            score += 10.0
        if has_dates:
            score += 10.0

        score = round(min(100.0, score), 1)

        return {
            "score": score,
            "experience_entries_count": entries_count,
            "total_bullet_points": bullet_count,
            "has_employment_dates": has_dates
        }

    def analyze_content_quality(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check content quality indicators:
        - Presence of powerful action verbs
        - Quantified metrics & achievements (numbers, %, $)
        - Summary length & impact
        - Bullet point concise formatting
        """
        text_all = self._extract_all_text(resume_data)
        
        # 1. Action verbs count
        verbs_found = []
        for verb in ACHIEVEMENT_VERBS:
            if re.search(r'\b' + re.escape(verb.lower()) + r'\b', text_all.lower()):
                verbs_found.append(verb)

        action_verb_score = min(100.0, len(verbs_found) * 15.0)

        # 2. Quantified achievements (% / $ / numbers)
        metrics_found = re.findall(r'\b\d+(?:%|\+|\s*k|\s*m)?\b|\$', text_all)
        quantified_score = min(100.0, len(metrics_found) * 20.0)

        # 3. Summary length check
        summary = str(resume_data.get("summary", "") or resume_data.get("objective", "")).strip()
        summary_word_count = len(summary.split()) if summary else 0
        summary_score = 100.0 if (20 <= summary_word_count <= 100) else (50.0 if summary_word_count > 0 else 0.0)

        # Weighted content quality score
        score = (action_verb_score * 0.40) + (quantified_score * 0.40) + (summary_score * 0.20)
        score = round(min(100.0, max(0.0, score)), 1)

        return {
            "score": score,
            "action_verbs_found": list(set(verbs_found)),
            "action_verbs_count": len(set(verbs_found)),
            "quantified_metrics_count": len(metrics_found),
            "summary_word_count": summary_word_count,
            "summary_quality_pass": summary_word_count >= 20
        }

    def _to_dict(self, resume_data: Any) -> Dict[str, Any]:
        """Convert resume_data model or dict to standard dict."""
        if hasattr(resume_data, "to_dict"):
            return resume_data.to_dict()
        elif hasattr(resume_data, "dict"):
            return resume_data.dict()
        elif hasattr(resume_data, "model_dump"):
            return resume_data.model_dump()
        elif isinstance(resume_data, dict):
            return resume_data
        return {}

    def _extract_all_text(self, data: Dict[str, Any]) -> str:
        """Flatten all dictionary fields into a single string for text matching."""
        parts: List[str] = []

        def _walk(obj: Any):
            if isinstance(obj, str):
                parts.append(obj)
            elif isinstance(obj, list):
                for item in obj:
                    _walk(item)
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    if k not in ["contains_tables", "contains_graphics"]:
                        _walk(v)

        _walk(data)
        return " ".join(parts)

    def _extract_skills_list(self, data: Dict[str, Any]) -> List[str]:
        """Extract flat list of skills from resume dictionary."""
        skills = data.get("skills", [])
        if isinstance(skills, list):
            return [str(s).strip() for s in skills if s]
        elif isinstance(skills, dict):
            flat = []
            for sub in skills.values():
                if isinstance(sub, list):
                    flat.extend([str(s).strip() for s in sub if s])
            return flat
        return []

    def _calculate_grade(self, score: float) -> str:
        """Map score 0-100 to letter grade."""
        if score >= 90.0:
            return "A+"
        elif score >= 85.0:
            return "A"
        elif score >= 75.0:
            return "B"
        elif score >= 65.0:
            return "C"
        elif score >= 50.0:
            return "D"
        return "F"

    def _collect_suggestions(
        self,
        sections_res: Dict[str, Any],
        formatting_res: Dict[str, Any],
        keyword_res: Dict[str, Any],
        skills_rel_res: Dict[str, Any],
        exp_rel_res: Dict[str, Any],
        quality_res: Dict[str, Any]
    ) -> List[str]:
        """Aggregate high-value suggestions across all sub-analyses."""
        suggestions: List[str] = []

        if sections_res.get("missing_sections"):
            missing = ", ".join(sections_res["missing_sections"])
            suggestions.append(f"Add missing ATS sections: {missing}.")

        if formatting_res.get("issues"):
            suggestions.extend(formatting_res["issues"])

        if keyword_res.get("missing_keywords"):
            top_missing = ", ".join(keyword_res["missing_keywords"][:5])
            suggestions.append(f"Incorporate missing job keywords: {top_missing}.")

        if quality_res.get("action_verbs_count", 0) < 3:
            suggestions.append("Use strong action verbs (e.g., Spearheaded, Architected, Optimized) to start work experience bullet points.")

        if quality_res.get("quantified_metrics_count", 0) < 2:
            suggestions.append("Quantify your achievements with measurable numbers, percentages, or metrics.")

        return suggestions


def analyze_resume(
    resume_data: Union[Dict[str, Any], Any],
    job_data: Optional[Union[Dict[str, Any], str, Any]] = None
) -> ATSAnalysisResult:
    """Convenience function to run ATS resume analysis."""
    engine = ATSEngine()
    return engine.analyze_resume(resume_data, job_data)


def check_sections(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to check section completeness."""
    engine = ATSEngine()
    return engine.check_sections(resume_data)


def check_formatting(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to check ATS formatting compliance."""
    engine = ATSEngine()
    return engine.check_formatting(resume_data)


def analyze_keywords(
    resume_data: Dict[str, Any],
    job_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Convenience function to analyze keyword alignment."""
    engine = ATSEngine()
    return engine.analyze_keywords(resume_data, job_data)


def analyze_content_quality(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to evaluate content quality metrics."""
    engine = ATSEngine()
    return engine.analyze_content_quality(resume_data)
