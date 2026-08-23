"""
Utility modules for SmartResume AI.

Re-exports security, validation, and helper functions for convenient top-level access.
"""

from .helpers import (
    SKILL_ALIASES,
    TIMEZONES,
    calculate_experience_years,
    extract_keywords_from_text,
    format_date,
    format_score,
    generate_id,
    normalize_skill,
    paginate_results,
)
from .security import (
    create_access_token,
    get_current_user,
    hash_password,
    oauth2_scheme,
    pwd_context,
    verify_password,
)
from .validators import (
    sanitize_input,
    validate_email,
    validate_password,
    validate_phone,
    validate_resume_data,
    validate_url,
)

__all__ = [
    # Security utilities
    "pwd_context",
    "hash_password",
    "verify_password",
    "create_access_token",
    "get_current_user",
    "oauth2_scheme",
    # Validation utilities
    "validate_email",
    "validate_password",
    "validate_phone",
    "validate_url",
    "sanitize_input",
    "validate_resume_data",
    # Helper utilities
    "generate_id",
    "format_date",
    "calculate_experience_years",
    "normalize_skill",
    "extract_keywords_from_text",
    "format_score",
    "SKILL_ALIASES",
    "TIMEZONES",
    "paginate_results",
]
