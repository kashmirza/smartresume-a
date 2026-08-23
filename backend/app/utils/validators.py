"""
Validation and sanitization utilities for SmartResume AI.

Provides input validation for email addresses, passwords, phone numbers, URLs,
and structured resume data, along with input sanitization against XSS attacks.
"""

import html
import re
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse


def validate_email(email: str) -> bool:
    """Validate an email address using regex.

    Args:
        email: Email address string to validate.

    Returns:
        True if email format is valid, False otherwise.
    """
    if not email or not isinstance(email, str):
        return False

    email = email.strip()
    if len(email) > 254:
        return False

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password(password: str) -> bool:
    """Validate password strength according to security policy.

    Policy: Minimum 8 characters, at least 1 uppercase letter, and at least 1 numeric digit.

    Args:
        password: Password string to validate.

    Returns:
        True if password meets all requirements, False otherwise.
    """
    if not password or not isinstance(password, str):
        return False

    if len(password) < 8:
        return False

    has_uppercase = bool(re.search(r"[A-Z]", password))
    has_number = bool(re.search(r"[0-9]", password))

    return has_uppercase and has_number


def validate_phone(phone: str) -> bool:
    """Validate a phone number string.

    Supports international prefixes (+), spaces, hyphens, periods, and parentheses.
    Ensures total digit count is between 7 and 15 digits (E.164 standard).

    Args:
        phone: Phone number string to validate.

    Returns:
        True if phone format is valid, False otherwise.
    """
    if not phone or not isinstance(phone, str):
        return False

    phone = phone.strip()
    if not phone:
        return False

    # Structure check allowing international format characters
    pattern = r"^\+?[0-9\s\-\(\)\.]{7,20}$"
    if not re.match(pattern, phone):
        return False

    # Digit count check (7 to 15 digits)
    digits = re.sub(r"\D", "", phone)
    return 7 <= len(digits) <= 15


def validate_url(url: str) -> bool:
    """Validate a URL string for web schemes (http, https, or ftp).

    Args:
        url: URL string to validate.

    Returns:
        True if URL is valid, False otherwise.
    """
    if not url or not isinstance(url, str):
        return False

    url = url.strip()
    if not url:
        return False

    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https", "ftp"):
            return False
        if not parsed.netloc:
            return False

        url_pattern = r"^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$"
        return bool(re.match(url_pattern, url, re.IGNORECASE))
    except Exception:
        return False


def sanitize_input(text: str) -> str:
    """Sanitize input text by removing whitespace and stripping/escaping XSS constructs.

    Args:
        text: Input text string to sanitize.

    Returns:
        Cleaned and sanitized text string.
    """
    if text is None:
        return ""

    if not isinstance(text, str):
        text = str(text)

    # Strip leading and trailing whitespace
    text = text.strip()

    # Remove script, style, and iframe tags along with their inner contents
    text = re.sub(r"<(script|style|iframe)[^>]*>.*?</\1>", "", text, flags=re.IGNORECASE | re.DOTALL)

    # Remove inline event attributes (e.g., onclick=..., onload=...)
    text = re.sub(r"\bon\w+\s*=\s*(['\"][^'\"]*['\"]|\S+)", "", text, flags=re.IGNORECASE)

    # Strip dangerous URI schemes
    text = re.sub(r"javascript\s*:", "", text, flags=re.IGNORECASE)
    text = re.sub(r"vbscript\s*:", "", text, flags=re.IGNORECASE)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Escape HTML special characters for security
    text = html.escape(text, quote=True)

    return text.strip()


def validate_resume_data(resume_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a structured resume data dictionary against required schema and formats.

    Args:
        resume_data: Dictionary containing resume sections (personal_info, experience, education, skills).

    Returns:
        Tuple of (is_valid: bool, errors: List[str]).
    """
    errors: List[str] = []

    if not resume_data or not isinstance(resume_data, dict):
        return False, ["Resume data must be a non-empty dictionary object."]

    # 1. Validate Personal Information / Contact Section
    personal_info = resume_data.get("personal_info") or resume_data.get("contact") or resume_data
    if isinstance(personal_info, dict):
        email = personal_info.get("email")
        if email and not validate_email(str(email)):
            errors.append(f"Invalid email address format: '{email}'.")

        phone = personal_info.get("phone")
        if phone and not validate_phone(str(phone)):
            errors.append(f"Invalid phone number format: '{phone}'.")

        for url_key in ("website", "portfolio", "linkedin", "github", "url"):
            url_val = personal_info.get(url_key)
            if url_val and not validate_url(str(url_val)):
                errors.append(f"Invalid URL for '{url_key}': '{url_val}'.")
    else:
        errors.append("'personal_info' section must be a dictionary.")

    # 2. Validate Experience Section
    experience = resume_data.get("experience") or resume_data.get("work_experience")
    if experience is not None:
        if not isinstance(experience, list):
            errors.append("'experience' section must be a list of work history entries.")
        else:
            for idx, item in enumerate(experience):
                if not isinstance(item, dict):
                    errors.append(f"Experience entry at index {idx} must be an object.")
                    continue
                if not item.get("title") and not item.get("position") and not item.get("role"):
                    errors.append(f"Experience entry at index {idx} is missing a job title or position.")
                if not item.get("company") and not item.get("organization"):
                    errors.append(f"Experience entry at index {idx} is missing a company or organization name.")

    # 3. Validate Education Section
    education = resume_data.get("education")
    if education is not None:
        if not isinstance(education, list):
            errors.append("'education' section must be a list of education entries.")
        else:
            for idx, item in enumerate(education):
                if not isinstance(item, dict):
                    errors.append(f"Education entry at index {idx} must be an object.")
                    continue
                if not item.get("institution") and not item.get("school") and not item.get("university"):
                    errors.append(f"Education entry at index {idx} is missing an institution or school name.")
                if not item.get("degree") and not item.get("field_of_study"):
                    errors.append(f"Education entry at index {idx} is missing a degree or field of study.")

    # 4. Validate Skills Section
    skills = resume_data.get("skills")
    if skills is not None:
        if not isinstance(skills, (list, dict)):
            errors.append("'skills' section must be a list or dictionary object.")

    is_valid = len(errors) == 0
    return is_valid, errors
