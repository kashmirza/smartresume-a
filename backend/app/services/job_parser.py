"""
Job Description Analyzer for SmartResume AI.

Extracts key information from job descriptions including required/preferred skills,
experience requirements, education expectations, job titles, and keywords.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Set
import re


SKILLS_DATABASE: Dict[str, List[str]] = {
    "programming_languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang",
        "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "perl",
        "shell", "bash", "powershell", "sql", "html", "css", "sass", "less", "dart",
        "assembly", "haskell", "elixir", "lua"
    ],
    "frameworks": [
        "fastapi", "django", "flask", "react", "react.js", "reactjs", "next.js", "nextjs",
        "vue", "vue.js", "vuejs", "angular", "express", "express.js", "node.js", "nodejs",
        "spring", "spring boot", ".net", "asp.net", "entity framework", "laravel", "symfony",
        "ruby on rails", "rails", "flutter", "react native", "tailwind", "tailwind css",
        "bootstrap", "material ui", "chakra ui", "svelte", "gatsby", "nuxt", "nest.js", "nestjs",
        "fastify", "pytorhc", "pytorch", "tensorflow", "keras", "scikit-learn", "pandas", "numpy"
    ],
    "databases": [
        "postgresql", "postgres", "mysql", "mongodb", "redis", "sqlite", "elasticsearch",
        "dynamodb", "cassandra", "oracle", "sql server", "mssql", "mariadb", "neo4j",
        "cockroachdb", "clickhouse", "snowflake", "bigquery", "redshift", "supabase", "firebase"
    ],
    "tools": [
        "git", "github", "gitlab", "bitbucket", "docker", "kubernetes", "k8s", "jenkins",
        "github actions", "gitlab ci", "circleci", "terraform", "ansible", "pulumi",
        "jira", "confluence", "postman", "swagger", "openapi", "webpack", "vite", "babel",
        "npm", "yarn", "pnpm", "pip", "poetry", "datadog", "new relic", "prometheus",
        "grafana", "sentry", "splunk", "kafka", "rabbitmq"
    ],
    "cloud_platforms": [
        "aws", "amazon web services", "azure", "microsoft azure", "gcp", "google cloud",
        "google cloud platform", "heroku", "digitalocean", "vercel", "netlify", "cloudflare",
        "serverless", "lambda", "ecs", "eks", "s3", "ec2", "cloudformation"
    ],
    "soft_skills": [
        "communication", "leadership", "problem solving", "teamwork", "critical thinking",
        "time management", "collaboration", "adaptability", "creativity", "work ethic",
        "conflict resolution", "mentorship", "project management", "stakeholder management",
        "decision making", "interpersonal skills", "analytical skills"
    ],
    "methodologies": [
        "agile", "scrum", "kanban", "ci/cd", "devops", "tdd", "test driven development",
        "bdd", "microservices", "rest api", "restful api", "graphql", "grpc", "soap",
        "event driven architecture", "domain driven design", "ddd", "pair programming",
        "code review", "system design", "oop", "functional programming"
    ]
}


@dataclass
class JobAnalysis:
    """Data class representing analyzed job description details."""
    job_title: str
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    experience_required: Dict[str, Any] = field(default_factory=dict)
    education_required: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    categorized_skills: Dict[str, List[str]] = field(default_factory=dict)
    raw_text: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert JobAnalysis instance to dictionary."""
        return asdict(self)


class JobParser:
    """Production job description parsing and analysis engine."""

    def __init__(self, skills_db: Optional[Dict[str, List[str]]] = None):
        """Initialize parser with optional custom skills database."""
        self.skills_db = skills_db or SKILLS_DATABASE
        self._flat_skills_map: Dict[str, str] = {}
        self._build_skills_map()

    def _build_skills_map(self) -> None:
        """Create a lookup map mapping normalized skill names to standard database names."""
        for category, skills in self.skills_db.items():
            for skill in skills:
                normalized = skill.lower().strip()
                self._flat_skills_map[normalized] = skill

    def parse_job_description(self, description: str) -> JobAnalysis:
        """
        Parse job description text and extract structured job analysis.

        Args:

            description: Raw text of the job description.

        Returns:
            JobAnalysis object containing extracted insights.
        """
        if not description or not description.strip():
            return JobAnalysis(job_title="Unknown Position", raw_text=description or "")

        clean_text = description.strip()

        job_title = self.extract_job_title(clean_text)
        required_skills, preferred_skills, categorized = self.extract_skills(clean_text)
        experience_req = self.extract_experience(clean_text)
        education_req = self.extract_education(clean_text)
        keywords = self.extract_keywords(clean_text, required_skills + preferred_skills)

        return JobAnalysis(
            job_title=job_title,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            experience_required=experience_req,
            education_required=education_req,
            keywords=keywords,
            categorized_skills=categorized,
            raw_text=clean_text
        )

    def extract_job_title(self, text: str) -> str:
        """Extract job title from description text."""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Check first 3 lines for explicit job title patterns
        title_patterns = [
            r'^(?:Job Title|Position|Role):\s*(.+)$',
            r'^Looking for a\s+(.+)$',
            r'^We are hiring a\s+(.+)$',
            r'^Hiring:\s*(.+)$'
        ]

        for line in lines[:5]:
            for pattern in title_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    return match.group(1).strip()

        # Fallback: look for common title words in early lines
        role_keywords = [
            'developer', 'engineer', 'architect', 'manager', 'lead', 'designer',
            'analyst', 'data scientist', 'administrator', 'consultant', 'specialist',
            'full stack', 'backend', 'frontend', 'devops', 'product manager'
        ]

        for line in lines[:3]:
            if len(line) < 80 and any(keyword in line.lower() for keyword in role_keywords):
                # Clean up punctuation
                cleaned = re.sub(r'^[#*\-\s]+', '', line).strip()
                if cleaned:
                    return cleaned

        return lines[0][:60] if lines else "Software Engineer"

    def extract_skills(self, text: str) -> tuple[List[str], List[str], Dict[str, List[str]]]:
        """
        Extract required and preferred skills, categorized by domain.

        Returns:
            Tuple of (required_skills, preferred_skills, categorized_skills)
        """
        sections = self._split_into_sections(text)
        
        all_matched_skills: Set[str] = set()
        categorized: Dict[str, List[str]] = {cat: [] for cat in self.skills_db}

        # Match skills across text using exact & regex word boundary logic
        lowered_text = text.lower()

        for category, skills in self.skills_db.items():
            for skill in skills:
                pattern = r'(?:\b|_)' + re.escape(skill.lower()) + r'(?:\b|_)'
                # Special handling for C++, C#, .NET
                if skill.lower() in ['c++', 'c#', '.net', 'next.js', 'vue.js', 'node.js', 'express.js']:
                    pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill.lower()) + r'(?![a-zA-Z0-9])'

                if re.search(pattern, lowered_text):
                    all_matched_skills.add(skill)
                    if skill not in categorized[category]:
                        categorized[category].append(skill)

        # Distinguish required vs preferred based on sections
        preferred_skills: Set[str] = set()
        required_skills: Set[str] = set()

        pref_section_text = " ".join(sections.get("preferred", [])).lower()
        req_section_text = " ".join(sections.get("required", [])).lower()

        for skill in all_matched_skills:
            skill_lower = skill.lower()
            in_pref = skill_lower in pref_section_text
            in_req = skill_lower in req_section_text

            if in_pref and not in_req:
                preferred_skills.add(skill)
            else:
                required_skills.add(skill)

        # Remove empty categories
        categorized = {k: v for k, v in categorized.items() if v}

        return sorted(list(required_skills)), sorted(list(preferred_skills)), categorized

    def _split_into_sections(self, text: str) -> Dict[str, List[str]]:
        """Separate description text into required vs preferred sections."""
        lines = text.split('\n')
        sections: Dict[str, List[str]] = {"required": [], "preferred": [], "general": []}
        current_section = "general"

        req_keywords = ['requirement', 'must have', 'required', 'qualifications', 'what you bring', 'who you are']
        pref_keywords = ['preferred', 'nice to have', 'bonus', 'plus', 'desired', 'good to have']

        for line in lines:
            line_lower = line.lower().strip()
            if any(k in line_lower for k in pref_keywords):
                current_section = "preferred"
            elif any(k in line_lower for k in req_keywords):
                current_section = "required"

            sections[current_section].append(line)

        return sections

    def extract_experience(self, text: str) -> Dict[str, Any]:
        """
        Extract required years of experience from job text.

        Returns:
            Dict containing min_years, max_years, summary_string, raw_matches
        """
        patterns = [
            r'(\d+)\s*\+\s*(?:-\s*\d+\s*)?(?:years?|yrs?)(?:\s+of)?\s+(?:relevant\s+)?(?:experience|exp)',
            r'(\d+)\s*(?:to|-)\s*(\d+)\s*(?:years?|yrs?)(?:\s+of)?\s+(?:relevant\s+)?(?:experience|exp)',
            r'(?:minimum|at least|over)\s+(\d+)\s+(?:years?|yrs?)(?:\s+of)?\s+(?:relevant\s+)?(?:experience|exp)',
            r'(\d+)\s*(?:years?|yrs?)\s+experience',
            r'(\d+)\s*(?:years?|yrs?)\s+(?:in|with|of)'
        ]

        min_years = 0
        max_years = None
        matches = []

        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                full_match = match.group(0)
                matches.append(full_match)
                groups = match.groups()
                
                if len(groups) >= 1 and groups[0]:
                    y1 = int(groups[0])
                    if y1 > min_years:
                        min_years = y1
                if len(groups) >= 2 and groups[1]:
                    max_years = int(groups[1])

        summary = f"{min_years}+ years of experience" if min_years > 0 else "Not explicitly specified"
        if min_years > 0 and max_years:
            summary = f"{min_years}-{max_years} years of experience"

        return {
            "min_years": min_years,
            "max_years": max_years,
            "summary": summary,
            "raw_matches": matches
        }

    def extract_education(self, text: str) -> List[str]:
        """Extract education requirements from text."""
        education_keywords = [
            r"(?:bachelor'?s?|bs|ba|b\.s\.|b\.a\.)(?:\s+degree)?(?:\s+in\s+[\w\s]+)?",
            r"(?:master'?s?|ms|ma|m\.s\.|m\.a\.)(?:\s+degree)?(?:\s+in\s+[\w\s]+)?",
            r"(?:phd|doctorate|ph\.d\.)(?:\s+in\s+[\w\s]+)?",
            r"degree in computer science",
            r"degree in software engineering",
            r"equivalent practical experience"
        ]

        results = []
        for pattern in education_keywords:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                matched_str = match.group(0).strip()
                if matched_str not in results:
                    results.append(matched_str)

        if not results:
            if re.search(r'\bdegree\b', text, re.IGNORECASE):
                results.append("Degree in Computer Science, Engineering or related field")

        return results

    def extract_keywords(self, text: str, extracted_skills: List[str]) -> List[str]:
        """Extract top industry & technical keywords from the job description."""
        stop_words = {
            'the', 'and', 'to', 'of', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this',
            'with', 'i', 'you', 'it', 'not', 'or', 'be', 'are', 'from', 'at', 'as', 'your',
            'all', 'have', 'new', 'more', 'an', 'was', 'we', 'will', 'home', 'can', 'us',
            'about', 'if', 'page', 'my', 'has', 'search', 'free', 'but', 'our', 'one',
            'other', 'do', 'no', 'information', 'time', 'they', 'site', 'he', 'up', 'may',
            'what', 'which', 'their', 'news', 'out', 'use', 'any', 'there', 'see', 'only',
            'so', 'his', 'when', 'contact', 'here', 'business', 'who', 'web', 'also',
            'now', 'help', 'get', 'pm', 'view', 'online', 'first', 'am', 'been', 'would',
            'how', 'were', 'me', 'services', 'some', 'these', 'click', 'its', 'like',
            'service', 'than', 'find', 'price', 'date', 'back', 'top', 'people', 'had',
            'list', 'name', 'just', 'over', 'state', 'year', 'day', 'into', 'email',
            'two', 'health', 'world', 're', 'next', 'used', 'go', 'work', 'last', 'most',
            'products', 'music', 'buy', 'data', 'make', 'them', 'should', 'product',
            'system', 'post', 'her', 'city', 'add', 'policy', 'number', 'such', 'please',
            'available', 'copyright', 'support', 'message', 'after', 'best', 'software',
            'then', 'jan', 'good', 'well', 'where', 'info', 'rights', 'public', 'books',
            'high', 'school', 'through', 'm', 'each', 'links', 'she', 'very', 'off',
            'looking', 'role', 'position', 'team', 'company', 'candidate', 'join'
        }

        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        word_counts: Dict[str, int] = {}
        for w in words:
            if w not in stop_words:
                word_counts[w] = word_counts.get(w, 0) + 1

        top_words = sorted(word_counts.keys(), key=lambda w: word_counts[w], reverse=True)[:15]

        # Combine extracted technical skills + top domain keywords
        combined = list(dict.fromkeys(extracted_skills + top_words))
        return combined[:25]


def parse_job_description(description: str) -> JobAnalysis:
    """Convenience wrapper function to parse job description text."""
    parser = JobParser()
    return parser.parse_job_description(description)
