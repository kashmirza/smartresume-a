"""
Helper utilities for SmartResume AI.

Provides ID generation, date formatting, total experience calculation, skill normalization,
keyword extraction from job/resume text, score formatting, timezone list, and pagination.
"""

from datetime import datetime
import math
import re
from typing import Any, Dict, List, Optional, Union
import uuid

# Canonical mapping for normalizing skill name variations and aliases
SKILL_ALIASES: Dict[str, str] = {
    # JavaScript & Frontend Ecosystem
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "react": "React",
    "reactjs": "React",
    "react.js": "React",
    "native": "React Native",
    "react native": "React Native",
    "react-native": "React Native",
    "vue": "Vue.js",
    "vuejs": "Vue.js",
    "vue.js": "Vue.js",
    "angular": "Angular",
    "angularjs": "Angular",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "express": "Express.js",
    "expressjs": "Express.js",
    "next": "Next.js",
    "nextjs": "Next.js",
    "next.js": "Next.js",
    "nuxt": "Nuxt.js",
    "nuxtjs": "Nuxt.js",
    "tailwind": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",
    "tail-wind": "Tailwind CSS",
    "bootstrap": "Bootstrap",
    # Python & Data Science / ML
    "py": "Python",
    "python": "Python",
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "dl": "Deep Learning",
    "nlp": "Natural Language Processing",
    "cv": "Computer Vision",
    # Programming Languages
    "cpp": "C++",
    "c++": "C++",
    "c#": "C#",
    "csharp": "C#",
    "golang": "Go",
    "go": "Go",
    "rs": "Rust",
    "rust": "Rust",
    "rb": "Ruby",
    "ruby": "Ruby",
    "rails": "Ruby on Rails",
    "ror": "Ruby on Rails",
    "kt": "Kotlin",
    "kotlin": "Kotlin",
    "java": "Java",
    # Databases & Cloud Infrastructure
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "pg": "PostgreSQL",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "mysql": "MySQL",
    "redis": "Redis",
    "aws": "Amazon Web Services",
    "gcp": "Google Cloud Platform",
    "azure": "Microsoft Azure",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "docker": "Docker",
    # Frameworks, Tools & Protocols
    "rest": "REST API",
    "restful": "REST API",
    "graphql": "GraphQL",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "html": "HTML",
    "html5": "HTML",
    "css": "CSS",
    "css3": "CSS",
    "sass": "SASS",
    "scss": "SASS",
}

# Standard list of common IANA timezones
TIMEZONES: List[str] = [
    "UTC",
    "Africa/Cairo",
    "Africa/Johannesburg",
    "Africa/Lagos",
    "America/Anchorage",
    "America/Argentina/Buenos_Aires",
    "America/Bogota",
    "America/Chicago",
    "America/Denver",
    "America/Los_Angeles",
    "America/Mexico_City",
    "America/New_York",
    "America/Phoenix",
    "America/Santiago",
    "America/Sao_Paulo",
    "America/Toronto",
    "America/Vancouver",
    "Asia/Bangkok",
    "Asia/Dubai",
    "Asia/Hong_Kong",
    "Asia/Istanbul",
    "Asia/Jakarta",
    "Asia/Karachi",
    "Asia/Kolkata",
    "Asia/Riyadh",
    "Asia/Seoul",
    "Asia/Shanghai",
    "Asia/Singapore",
    "Asia/Tokyo",
    "Australia/Melbourne",
    "Australia/Sydney",
    "Europe/Amsterdam",
    "Europe/Athens",
    "Europe/Berlin",
    "Europe/Brussels",
    "Europe/Dublin",
    "Europe/London",
    "Europe/Madrid",
    "Europe/Moscow",
    "Europe/Paris",
    "Europe/Rome",
    "Europe/Zurich",
    "Pacific/Auckland",
    "Pacific/Honolulu",
]

# Stop words to filter out during keyword extraction
COMMON_STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "cannot", "could", "did",
    "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further",
    "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him",
    "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself",
    "just", "me", "more", "most", "my", "myself", "no", "nor", "not", "of", "off",
    "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over",
    "own", "same", "she", "should", "so", "some", "such", "than", "that", "the",
    "their", "theirs", "them", "themselves", "then", "there", "these", "they",
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why",
    "with", "would", "you", "your", "yours", "yourself", "yourselves", "using",
    "used", "work", "worked", "working", "responsible", "experience", "ability",
    "knowledge", "skills", "strong", "team", "years", "including", "within",
}


def generate_id() -> str:
    """Generate a unique UUID v4 string.

    Returns:
        String representation of a random UUID v4.
    """
    return str(uuid.uuid4())


def format_date(date_str: str, output_format: str = "%B %Y") -> str:
    """Format a date string into a clean, human-readable date.

    Supports inputs such as 'YYYY-MM-DD', 'YYYY-MM', 'MM/YYYY', 'YYYY', and ISO datetimes.

    Args:
        date_str: Input raw date string.
        output_format: Desired strftime format (default: '%B %Y', e.g. 'January 2023').

    Returns:
        Formatted date string, or original string if parsing is not possible.
    """
    if not date_str or not isinstance(date_str, str):
        return ""

    cleaned = date_str.strip()
    if cleaned.lower() in ("present", "current", "now", "today"):
        return "Present"

    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m",
        "%m/%Y",
        "%m/%d/%Y",
        "%b %Y",
        "%B %Y",
        "%Y",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(cleaned, fmt)
            return dt.strftime(output_format)
        except ValueError:
            continue

    return cleaned


def calculate_experience_years(experience_list: list) -> float:
    """Calculate total years of professional experience from a list of experience entries.

    Each entry dictionary may contain 'start_date', 'end_date', and/or 'is_current'.

    Args:
        experience_list: List of experience entry dictionaries.

    Returns:
        Total cumulative experience in years, rounded to 1 decimal place.
    """
    if not experience_list or not isinstance(experience_list, list):
        return 0.0

    total_days = 0.0
    now = datetime.now()

    def parse_exp_date(d_val: Any) -> Optional[datetime]:
        if not d_val or not isinstance(d_val, str):
            return None
        cleaned = d_val.strip()
        if cleaned.lower() in ("present", "current", "now", "today"):
            return now
        for fmt in ("%Y-%m-%d", "%Y-%m", "%m/%Y", "%m/%d/%Y", "%Y"):
            try:
                return datetime.strptime(cleaned, fmt)
            except ValueError:
                continue
        return None

    for entry in experience_list:
        if not isinstance(entry, dict):
            continue

        start = parse_exp_date(entry.get("start_date"))
        is_current = entry.get("is_current") or entry.get("current", False)

        if is_current:
            end = now
        else:
            end = parse_exp_date(entry.get("end_date")) or now

        if start and end and end >= start:
            duration = (end - start).days
            total_days += duration

    years = total_days / 365.25
    return round(years, 1)


def normalize_skill(skill_name: str) -> str:
    """Normalize skill name using SKILL_ALIASES mapping or standard formatting.

    Args:
        skill_name: Raw skill string (e.g. 'js', 'ReactJS', 'PY').

    Returns:
        Normalized canonical skill string (e.g. 'JavaScript', 'React', 'Python').
    """
    if not skill_name or not isinstance(skill_name, str):
        return ""

    cleaned = skill_name.strip()
    key = cleaned.lower()

    if key in SKILL_ALIASES:
        return SKILL_ALIASES[key]

    return cleaned


def extract_keywords_from_text(text: str) -> List[str]:
    """Extract key technical and industry terms from text for ATS matching.

    Args:
        text: Raw text string (e.g., job description or resume summary).

    Returns:
        Deduplicated list of extracted keywords.
    """
    if not text or not isinstance(text, str):
        return []

    # Tokenize words retaining technical characters (+, #, ., /, -)
    tokens = re.findall(r"\b[a-zA-Z0-9\+#\.\/\-]{2,}\b", text)

    keywords: List[str] = []
    seen = set()

    for token in tokens:
        cleaned_token = token.strip(".,/-")
        lowered = cleaned_token.lower()

        if len(cleaned_token) < 2 or lowered in COMMON_STOP_WORDS:
            continue

        normalized = normalize_skill(cleaned_token)

        if normalized.lower() not in seen:
            seen.add(normalized.lower())
            keywords.append(normalized)

    return keywords


def format_score(breakdown_dict: dict) -> str:
    """Format an ATS score breakdown dictionary into a structured report string.

    Args:
        breakdown_dict: Dictionary containing overall score and category breakdown details.

    Returns:
        Formatted summary string report.
    """
    if not breakdown_dict or not isinstance(breakdown_dict, dict):
        return "No score data available."

    lines = [
        "========================================",
        "      ATS RESUME SCORE BREAKDOWN        ",
        "========================================",
    ]

    overall_score = breakdown_dict.get("overall_score") or breakdown_dict.get("overall") or breakdown_dict.get("score")
    if overall_score is not None:
        lines.append(f"Overall Match Score: {overall_score}/100")
        lines.append("-" * 40)

    categories = breakdown_dict.get("categories") or breakdown_dict.get("breakdown") or breakdown_dict
    if isinstance(categories, dict):
        lines.append("Category Breakdown:")
        for cat, score in categories.items():
            if cat in ("overall_score", "overall", "score", "feedback", "recommendations"):
                continue
            cat_name = cat.replace("_", " ").title()
            if isinstance(score, (int, float)):
                lines.append(f"  • {cat_name}: {score}%")
            elif isinstance(score, dict):
                sub_score = score.get("score", "N/A")
                detail = score.get("detail") or score.get("comments") or ""
                detail_str = f" ({detail})" if detail else ""
                lines.append(f"  • {cat_name}: {sub_score}%{detail_str}")
            else:
                lines.append(f"  • {cat_name}: {score}")

    feedback = breakdown_dict.get("feedback") or breakdown_dict.get("recommendations")
    if feedback:
        lines.append("-" * 40)
        lines.append("Feedback & Recommendations:")
        if isinstance(feedback, list):
            for item in feedback:
                lines.append(f"  - {item}")
        else:
            lines.append(f"  - {feedback}")

    lines.append("========================================")
    return "\n".join(lines)


def paginate_results(items: list, page: int = 1, per_page: int = 10) -> dict:
    """Paginate a list of items with pagination metadata.

    Args:
        items: List of items to paginate.
        page: Page number (1-indexed). Defaults to 1.
        per_page: Number of items per page. Defaults to 10.

    Returns:
        Dictionary containing paginated items and page metrics.
    """
    if not isinstance(items, list):
        items = []

    page = max(1, page)
    per_page = max(1, per_page)

    total = len(items)
    total_pages = max(1, math.ceil(total / per_page)) if total > 0 else 1

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_items = items[start_idx:end_idx]

    return {
        "items": paginated_items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
