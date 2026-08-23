"""
SmartResume AI Service Engine Package.

Exposes core ATS scoring, job description parsing, skill matching,
learning recommendations, resume optimization, and PDF/DOCX generation engines.
"""

from app.services.ats_engine import (
    ATSEngine,
    ATSAnalysisResult,
    analyze_resume,
    check_sections,
    check_formatting,
    analyze_keywords,
    analyze_content_quality,
)

from app.services.job_parser import (
    JobParser,
    JobAnalysis,
    parse_job_description,
    SKILLS_DATABASE,
)

from app.services.skill_matcher import (
    SkillMatcher,
    MatchResult,
    SkillGapResult,
    match_resume_to_job,
    analyze_skill_gap,
)

from app.services.recommendation import (
    RecommendationEngine,
    Recommendation,
    get_recommendations,
    get_learning_path,
    RECOMMENDATION_DATABASE,
)

from app.services.resume_optimizer import (
    ResumeOptimizer,
    optimize_summary,
    optimize_bullet_point,
    suggest_improvements,
    generate_professional_summary,
    ACHIEVEMENT_VERBS,
)

from app.services.pdf_generator import (
    PDFGenerator,
    generate_pdf,
    generate_docx,
)

__all__ = [
    # ATS Engine
    "ATSEngine",
    "ATSAnalysisResult",
    "analyze_resume",
    "check_sections",
    "check_formatting",
    "analyze_keywords",
    "analyze_content_quality",
    # Job Parser
    "JobParser",
    "JobAnalysis",
    "parse_job_description",
    "SKILLS_DATABASE",
    # Skill Matcher
    "SkillMatcher",
    "MatchResult",
    "SkillGapResult",
    "match_resume_to_job",
    "analyze_skill_gap",
    # Recommendation Engine
    "RecommendationEngine",
    "Recommendation",
    "get_recommendations",
    "get_learning_path",
    "RECOMMENDATION_DATABASE",
    # Resume Optimizer
    "ResumeOptimizer",
    "optimize_summary",
    "optimize_bullet_point",
    "suggest_improvements",
    "generate_professional_summary",
    "ACHIEVEMENT_VERBS",
    # PDF Generator
    "PDFGenerator",
    "generate_pdf",
    "generate_docx",
]
