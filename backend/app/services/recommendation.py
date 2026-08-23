"""
Learning & Skill Recommendation Engine for SmartResume AI.

Generates structured learning recommendations, projects, resource links,
and personalized step-by-step learning paths for identified skill gaps.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Union


@dataclass
class Recommendation:
    """Dataclass representing a learning recommendation for a single missing skill."""
    skill_name: str
    why_it_matters: str
    recommended_topics: List[str]
    suggested_project: Dict[str, Any]
    difficulty: str = "Intermediate"  # Beginner, Intermediate, Advanced
    estimated_hours: int = 20
    learning_resources: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert Recommendation instance to dictionary."""
        return asdict(self)


RECOMMENDATION_DATABASE: Dict[str, Dict[str, Any]] = {
    "Python": {
        "why_it_matters": "Python is a core language for backend development, data engineering, machine learning, and automation across tech industries.",
        "recommended_topics": [
            "Data structures, typing & OOP design patterns",
            "Asynchronous programming with asyncio & GIL concepts",
            "REST API building with FastAPI / Django",
            "Unit testing with pytest & mock objects"
        ],
        "suggested_project": {
            "title": "Async Task Processing Microservice",
            "description": "Build an asynchronous file processing API using Python 3.11+, FastAPI, and Redis queues with comprehensive pytest test coverage.",
            "deliverables": ["REST API code", "Test suite with >80% coverage", "Dockerized setup"]
        },
        "difficulty": "Intermediate",
        "estimated_hours": 25,
        "learning_resources": [
            {"title": "Official Python Docs", "url": "https://docs.python.org/3/"},
            {"title": "Real Python Tutorials", "url": "https://realpython.com/"}
        ]
    },
    "SQL": {
        "why_it_matters": "SQL is mandatory for querying relational databases, managing data persistence, and optimizing complex database operations.",
        "recommended_topics": [
            "Complex JOINs, subqueries, and window functions",
            "Indexing strategies & query execution plan optimization",
            "Database normalization & schema design",
            "Transactions, ACID compliance, and concurrency controls"
        ],
        "suggested_project": {
            "title": "E-Commerce Analytics & Reporting DB Schema",
            "description": "Design a relational database with 10+ tables, implement indexing, and write SQL scripts for analytical aggregation queries.",
            "deliverables": ["ER Diagram", "DDL/DML scripts", "Window function query benchmark"]
        },
        "difficulty": "Intermediate",
        "estimated_hours": 15,
        "learning_resources": [
            {"title": "Mode Analytics SQL Tutorial", "url": "https://mode.com/sql-tutorial/"},
            {"title": "SQLZoo Interactive Exercises", "url": "https://sqlzoo.net/"}
        ]
    },
    "Docker": {
        "why_it_matters": "Containerization with Docker is the industry standard for creating consistent runtime environments and simplifying CI/CD deployments.",
        "recommended_topics": [
            "Dockerfile best practices & multi-stage builds",
            "Docker Compose multi-container orchestration",
            "Networking, volume mounting & secret management",
            "Container security hardening & image size optimization"
        ],
        "suggested_project": {
            "title": "Containerized Full-Stack Web Application",
            "description": "Create a multi-container environment with frontend, API backend, PostgreSQL database, and NGINX reverse proxy using Docker Compose.",
            "deliverables": ["Production Dockerfiles", "docker-compose.yml", "Deployment documentation"]
        },
        "difficulty": "Intermediate",
        "estimated_hours": 18,
        "learning_resources": [
            {"title": "Docker Official Documentation", "url": "https://docs.docker.com/get-started/"},
            {"title": "Docker Deep Dive Guide", "url": "https://dockerlabs.collabnix.com/"}
        ]
    },
    "AWS": {
        "why_it_matters": "Amazon Web Services is the leading cloud provider powering backend infrastructure, serverless apps, and modern cloud architectures.",
        "recommended_topics": [
            "Compute: EC2, ECS, Lambda serverless functions",
            "Storage & DB: S3 bucket policies, RDS, DynamoDB",
            "Networking: VPC, Subnets, Route 53, CloudFront CDN",
            "IAM roles, policies, and security best practices"
        ],
        "suggested_project": {
            "title": "Serverless Document Processing Pipeline",
            "description": "Build an AWS Lambda architecture triggered by S3 file uploads that extracts metadata and stores records in DynamoDB.",
            "deliverables": ["CloudFormation / SAM / Terraform template", "Lambda function code", "Architecture diagram"]
        },
        "difficulty": "Advanced",
        "estimated_hours": 30,
        "learning_resources": [
            {"title": "AWS Skill Builder Free Courses", "url": "https://explore.skillbuilder.aws/"},
            {"title": "AWS Well-Architected Framework", "url": "https://aws.amazon.com/architecture/well-architected/"}
        ]
    },
    "FastAPI": {
        "why_it_matters": "FastAPI enables high-performance Python API development with automatic OpenAPI documentation and async execution.",
        "recommended_topics": [
            "Path & Query parameters, Pydantic data validation",
            "Dependency Injection system and authentication (OAuth2 / JWT)",
            "Async DB session handling with SQLAlchemy 2.0 / Tortoise ORM",
            "Middlewares, background tasks, and WebSocket endpoints"
        ],
        "suggested_project": {
            "title": "Secure Microservice with JWT Auth",
            "description": "Develop a REST API with FastAPI featuring JWT token authentication, rate limiting, Pydantic schemas, and interactive Swagger docs.",
            "deliverables": ["FastAPI source code", "OpenAPI schema spec", "Pytest API integration tests"]
        },
        "difficulty": "Intermediate",
        "estimated_hours": 15,
        "learning_resources": [
            {"title": "FastAPI Official Documentation", "url": "https://fastapi.tiangolo.com/"}
        ]
    },
    "React": {
        "why_it_matters": "React is the dominant UI library for building responsive, component-driven web applications.",
        "recommended_topics": [
            "Functional components, Hooks (useState, useEffect, useMemo, useCallback)",
            "State management with Context API, Redux Toolkit, or Zustand",
            "Component lifecycle, custom hooks & performance optimization",
            "Routing with React Router & client-side data fetching (React Query)"
        ],
        "suggested_project": {
            "title": "Interactive Analytics Dashboard",
            "description": "Build a multi-page React application with data visualization charts, dark mode toggle, and state persistence.",
            "deliverables": ["React application codebase", "Reusable component library", "Deploys on Vercel/Netlify"]
        },
        "difficulty": "Intermediate",
        "estimated_hours": 25,
        "learning_resources": [
            {"title": "React Official Documentation", "url": "https://react.dev/"}
        ]
    },
    "TypeScript": {
        "why_it_matters": "TypeScript adds static typing to JavaScript, catching errors early and powering robust large-scale applications.",
        "recommended_topics": [
            "Interfaces, Types, Generics, and Type Guards",
            "Strict mode configuration & compiler flags",
            "Integration with React / Node.js projects",
            "Advanced types: Union, Intersection, Mapped, and Conditional types"
        ],
        "suggested_project": {
            "title": "Type-Safe API Client SDK",
            "description": "Build a published NPM-ready TypeScript library with full generics, interfaces, and strict type safety.",
            "deliverables": ["TypeScript SDK source", "Compiled declaration files", "Usage examples"]
        },
        "difficulty": "Intermediate",
        "estimated_hours": 20,
        "learning_resources": [
            {"title": "TypeScript Official Handbook", "url": "https://www.typescriptlang.org/docs/"}
        ]
    },
    "PostgreSQL": {
        "why_it_matters": "PostgreSQL is the most powerful open-source relational database engine, renowned for reliability, extensibility, and JSON features.",
        "recommended_topics": [
            "Advanced SQL indexing (B-Tree, GIN, GiST)",
            "JSONB data handling & document queries",
            "Stored procedures, triggers, and PL/pgSQL",
            "Performance tuning, EXPLAIN ANALYZE, and connection pooling"
        ],
        "suggested_project": {
            "title": "High-Performance Data Storage Engine",
            "description": "Implement a PostgreSQL database with partitioned tables, custom indexes, and JSONB document columns for high-throughput tracking.",
            "deliverables": ["PostgreSQL migration scripts", "Benchmarking report", "EXPLAIN ANALYZE query breakdown"]
        },
        "difficulty": "Intermediate",
        "estimated_hours": 20,
        "learning_resources": [
            {"title": "PostgreSQL Official Docs", "url": "https://www.postgresql.org/docs/"}
        ]
    },
    "Kubernetes": {
        "why_it_matters": "Kubernetes automates deployment, scaling, and management of containerized applications in production environments.",
        "recommended_topics": [
            "Pods, Deployments, ReplicaSets, and Services",
            "ConfigMaps, Secrets, Persistent Volumes & Ingress controllers",
            "Helm package management & deployment manifests",
            "Cluster monitoring, metrics-server, and autoscaling (HPA)"
        ],
        "suggested_project": {
            "title": "Production Kubernetes Cluster Deployment",
            "description": "Deploy a scalable microservice application to Minikube or cloud Kubernetes cluster using Helm charts and ingress routing.",
            "deliverables": ["K8s YAML manifests", "Custom Helm chart", "Ingress setup documentation"]
        },
        "difficulty": "Advanced",
        "estimated_hours": 35,
        "learning_resources": [
            {"title": "Kubernetes Basics Documentation", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/"}
        ]
    },
    "Git": {
        "why_it_matters": "Git is the ubiquitous version control system required for software development, code collaboration, and CI/CD pipelines.",
        "recommended_topics": [
            "Branching models (Git Flow, Trunk-based development)",
            "Rebase, cherry-pick, stashing, and interactive rebase",
            "Resolving merge conflicts and commit squash practices",
            "Git hooks & GitHub Actions workflow integration"
        ],
        "suggested_project": {
            "title": "Collaborative Git Workflow Simulation",
            "description": "Demonstrate advanced Git operations: feature branches, PR code reviews, squashing, tag releases, and resolving merge conflicts.",
            "deliverables": ["GitHub repository with clean commit history", "Branch protection rules spec"]
        },
        "difficulty": "Beginner",
        "estimated_hours": 10,
        "learning_resources": [
            {"title": "Pro Git Book (Free)", "url": "https://git-scm.com/book/en/v2"}
        ]
    }
}


class RecommendationEngine:
    """Engine for generating learning recommendations and structured learning paths."""

    def __init__(self, database: Optional[Dict[str, Dict[str, Any]]] = None):
        """Initialize engine with recommendation database."""
        self.db = database or RECOMMENDATION_DATABASE

    def get_recommendations(self, missing_skills: List[str]) -> List[Recommendation]:
        """
        Generate detailed learning recommendations for a list of missing skills.

        Args:
            missing_skills: List of skill strings.

        Returns:
            List of Recommendation objects.
        """
        recommendations: List[Recommendation] = []

        for skill in missing_skills:
            if not skill or not skill.strip():
                continue

            normalized_key = self._find_matching_key(skill)
            if normalized_key and normalized_key in self.db:
                rec_data = self.db[normalized_key]
                recommendations.append(Recommendation(
                    skill_name=skill.strip(),
                    why_it_matters=rec_data["why_it_matters"],
                    recommended_topics=rec_data["recommended_topics"],
                    suggested_project=rec_data["suggested_project"],
                    difficulty=rec_data.get("difficulty", "Intermediate"),
                    estimated_hours=rec_data.get("estimated_hours", 20),
                    learning_resources=rec_data.get("learning_resources", [])
                ))
            else:
                # Dynamic fallback recommendation for unlisted skills
                recommendations.append(self._generate_fallback_recommendation(skill.strip()))

        return recommendations

    def _find_matching_key(self, skill: str) -> Optional[str]:
        """Find matching key in database handling case sensitivity and aliases."""
        skill_lower = skill.strip().lower()
        for key in self.db:
            if key.lower() == skill_lower:
                return key
        return None

    def _generate_fallback_recommendation(self, skill: str) -> Recommendation:
        """Generate structured recommendation for skills not explicitly in the pre-built DB."""
        return Recommendation(
            skill_name=skill,
            why_it_matters=f"{skill} is an essential technology requirement for target roles in modern software engineering.",
            recommended_topics=[
                f"Core concepts and architectural patterns of {skill}",
                f"Best practices and standard implementation patterns for {skill}",
                f"Testing, debugging, and performance optimization in {skill}",
                f"Integrating {skill} into existing software workflows"
            ],
            suggested_project={
                "title": f"Hands-on {skill} Implementation Project",
                "description": f"Build a practical hands-on application demonstrating proficiency in {skill} core concepts and API usage.",
                "deliverables": [f"Working {skill} project repository", "Documentation and setup guide"]
            },
            difficulty="Intermediate",
            estimated_hours=15,
            learning_resources=[
                {"title": f"Official {skill} Documentation", "url": f"https://www.google.com/search?q={skill}+official+docs"},
                {"title": f"{skill} Fundamentals Guide", "url": f"https://www.google.com/search?q={skill}+tutorial"}
            ]
        )

    def get_learning_path(self, skill_gaps: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
        """
        Suggest a structured learning order based on skill gap priorities and prerequisites.

        Args:
            skill_gaps: SkillGapResult object or dictionary containing priority gaps.

        Returns:
            Dict containing ordered steps, total estimated hours, and milestone timeline.
        """
        if hasattr(skill_gaps, 'to_dict'):
            gaps_dict = skill_gaps.to_dict()
        elif isinstance(skill_gaps, dict):
            gaps_dict = skill_gaps
        else:
            gaps_dict = {"high_priority_gaps": [], "medium_priority_gaps": [], "low_priority_gaps": []}

        high = gaps_dict.get("high_priority_gaps", [])
        medium = gaps_dict.get("medium_priority_gaps", [])
        low = gaps_dict.get("low_priority_gaps", [])

        # Priority ordering: HIGH -> MEDIUM -> LOW
        ordered_skills = high + medium + low
        all_recs = {rec.skill_name: rec for rec in self.get_recommendations(ordered_skills)}

        steps: List[Dict[str, Any]] = []
        cumulative_hours = 0
        phase = 1

        for skill in ordered_skills:
            rec = all_recs.get(skill)
            if not rec:
                continue

            priority = "HIGH" if skill in high else ("MEDIUM" if skill in medium else "LOW")
            cumulative_hours += rec.estimated_hours

            steps.append({
                "step_number": len(steps) + 1,
                "phase": f"Phase {phase}: {priority} Priority Focus",
                "skill": skill,
                "priority": priority,
                "estimated_hours": rec.estimated_hours,
                "cumulative_hours": cumulative_hours,
                "why_it_matters": rec.why_it_matters,
                "recommended_topics": rec.recommended_topics[:2],
                "suggested_project_title": rec.suggested_project.get("title", "")
            })

            if len(steps) % 2 == 0:
                phase += 1

        total_weeks = round(cumulative_hours / 10.0, 1)  # Assuming ~10 hrs/week study time

        return {
            "total_skills_to_learn": len(steps),
            "total_estimated_hours": cumulative_hours,
            "estimated_weeks_completion": total_weeks,
            "learning_path_steps": steps,
            "summary": f"Complete this {len(steps)}-skill roadmap (~{cumulative_hours} hrs / ~{total_weeks} weeks) to bridge your key job requirement gaps."
        }


def get_recommendations(missing_skills: List[str]) -> List[Recommendation]:
    """Convenience function to get recommendations for missing skills."""
    engine = RecommendationEngine()
    return engine.get_recommendations(missing_skills)


def get_learning_path(skill_gaps: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
    """Convenience function to construct a learning path from skill gaps."""
    engine = RecommendationEngine()
    return engine.get_learning_path(skill_gaps)
