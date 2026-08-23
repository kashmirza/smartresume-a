"""
SmartResume AI - ATS Classic Template Definition

This module provides layout definitions, styling rules, and rendering methods
for the ATS Classic template. The ATS Classic template is specifically designed
for 100% compatibility with Automated Applicant Tracking Systems (ATS).

Key Characteristics:
- Single-column layout
- Standard system fonts (Helvetica, Times-Roman, Arial)
- Clean, linear hierarchy without complex graphics, tables, floating boxes, or columns
- Standardized section titles (Work Experience, Education, Skills, Summary, Projects)
- High contrast, pure black text on crisp white background
"""

import re
from typing import Dict, Any, List, Optional


class ATSClassicTemplate:
    """
    ATS Classic Resume Template definition and renderer.
    Optimized for parsing accuracy across major ATS software (Greenhouse, Lever, Workday, Taleo).
    """

    TEMPLATE_ID = "ats_classic"
    NAME = "ATS Classic Standard"
    DESCRIPTION = "Single-column traditional layout optimized for 100% ATS parser compatibility and zero rendering errors."
    AUTHOR = "SmartResume AI Team"
    VERSION = "1.0.0"

    # Layout Rules & Specifications
    CONFIG = {
        "page_size": "LETTER",
        "margin_top_inches": 0.75,
        "margin_bottom_inches": 0.75,
        "margin_left_inches": 0.75,
        "margin_right_inches": 0.75,
        "font_family": "Helvetica",
        "font_size_name": 18,
        "font_size_title": 12,
        "font_size_heading": 13,
        "font_size_body": 10.5,
        "font_size_small": 9.5,
        "line_height_body": 1.25,
        "color_primary": "#000000",
        "color_secondary": "#222222",
        "color_text": "#111111",
        "allow_tables": False,
        "allow_columns": False,
        "allow_graphics": False,
    }

    STANDARD_SECTION_TITLES = {
        "summary": "PROFESSIONAL SUMMARY",
        "experience": "WORK EXPERIENCE",
        "education": "EDUCATION",
        "skills": "SKILLS & COMPETENCIES",
        "projects": "PROJECTS",
        "certifications": "CERTIFICATIONS & LICENSES",
        "languages": "LANGUAGES",
        "custom": "ADDITIONAL INFORMATION",
    }

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        """Initialize template with resume data dict."""
        self.data = data or {}

    def get_metadata(self) -> Dict[str, Any]:
        """Return template metadata."""
        return {
            "template_id": self.TEMPLATE_ID,
            "name": self.NAME,
            "description": self.DESCRIPTION,
            "version": self.VERSION,
            "ats_compatibility_score": 100,
            "features": [
                "Single-column design",
                "Standard header tags",
                "Standard bullet point formatting",
                "No graphics or multi-column containers",
                "Parseable by standard ATS engine",
            ],
            "config": self.CONFIG,
        }

    def format_contact_info(self, personal_info: Dict[str, Any]) -> str:
        """Format personal header into a clean ATS-parseable single line/block."""
        full_name = personal_info.get("full_name", "").upper()
        email = personal_info.get("email", "")
        phone = personal_info.get("phone", "")
        location = personal_info.get("location", "")
        linkedin = personal_info.get("linkedin_url", "")
        github = personal_info.get("github_url", "")
        website = personal_info.get("website_url", "")

        contact_parts = [p for p in [phone, email, location] if p]
        link_parts = [p for p in [linkedin, github, website] if p]

        lines = [f"<h1>{full_name}</h1>"]
        if contact_parts:
            lines.append(f"<p>{' | '.join(contact_parts)}</p>")
        if link_parts:
            lines.append(f"<p>{' | '.join(link_parts)}</p>")

        return "\n".join(lines)

    def render_html(self, data: Optional[Dict[str, Any]] = None) -> str:
        """
        Render resume data into clean HTML structured specifically for ReportLab / WeasyPrint conversion.
        """
        resume = data or self.data
        personal = resume.get("personal_info", {})
        summary = resume.get("summary", "")
        experiences = resume.get("work_experience", [])
        education = resume.get("education", [])
        skills = resume.get("skills", [])
        projects = resume.get("projects", [])
        certifications = resume.get("certifications", [])
        languages = resume.get("languages", [])

        html_out = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            '<meta charset="utf-8"/>',
            f"<title>{personal.get('full_name', 'Resume')}</title>",
            "<style>",
            "body { font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt; color: #000; line-height: 1.3; margin: 0.75in; }",
            "h1 { font-size: 18pt; text-align: center; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px; }",
            ".contact-bar { text-align: center; font-size: 10pt; margin-bottom: 12px; }",
            "h2 { font-size: 12pt; text-transform: uppercase; border-bottom: 1px solid #000; margin-top: 14px; margin-bottom: 6px; padding-bottom: 2px; }",
            ".exp-item, .edu-item, .proj-item { margin-bottom: 10px; }",
            ".item-header { display: flex; justify-content: space-between; font-weight: bold; }",
            ".item-subheader { display: flex; justify-content: space-between; font-style: italic; font-size: 10pt; margin-bottom: 4px; }",
            "ul { margin-top: 3px; margin-bottom: 6px; padding-left: 20px; }",
            "li { margin-bottom: 3px; }",
            ".skill-group { margin-bottom: 4px; }",
            "</style>",
            "</head>",
            "<body>",
        ]

        # Contact Info Header
        html_out.append(f"<h1>{personal.get('full_name', '')}</h1>")
        contact_items = []
        if personal.get("location"):
            contact_items.append(personal.get("location"))
        if personal.get("phone"):
            contact_items.append(personal.get("phone"))
        if personal.get("email"):
            contact_items.append(personal.get("email"))
        if personal.get("linkedin_url"):
            contact_items.append(personal.get("linkedin_url"))
        if personal.get("github_url"):
            contact_items.append(personal.get("github_url"))

        html_out.append(f'<div class="contact-bar">{" | ".join(contact_items)}</div>')

        # Summary Section
        if summary:
            html_out.append(f"<h2>{self.STANDARD_SECTION_TITLES['summary']}</h2>")
            html_out.append(f"<p>{summary}</p>")

        # Experience Section
        if experiences:
            html_out.append(f"<h2>{self.STANDARD_SECTION_TITLES['experience']}</h2>")
            for exp in experiences:
                html_out.append('<div class="exp-item">')
                date_str = f"{exp.get('start_date', '')} – {exp.get('end_date', 'Present')}"
                html_out.append(
                    f'<div class="item-header"><span>{exp.get("position_title", "")}</span><span>{date_str}</span></div>'
                )
                company_loc = f"{exp.get('company_name', '')}"
                if exp.get("location"):
                    company_loc += f" | {exp.get('location')}"
                html_out.append(f'<div class="item-subheader"><span>{company_loc}</span></div>')
                bullets = exp.get("bullet_points", [])
                if bullets:
                    html_out.append("<ul>")
                    for bullet in bullets:
                        html_out.append(f"<li>{bullet}</li>")
                    html_out.append("</ul>")
                html_out.append("</div>")

        # Education Section
        if education:
            html_out.append(f"<h2>{self.STANDARD_SECTION_TITLES['education']}</h2>")
            for edu in education:
                html_out.append('<div class="edu-item">')
                date_str = f"{edu.get('start_date', '')} – {edu.get('end_date', '')}"
                degree_field = f"{edu.get('degree', '')} in {edu.get('field_of_study', '')}"
                html_out.append(
                    f'<div class="item-header"><span>{edu.get("institution", "")}</span><span>{date_str}</span></div>'
                )
                html_out.append(f'<div class="item-subheader"><span>{degree_field}</span></div>')
                if edu.get("gpa"):
                    html_out.append(f"<p>GPA: {edu.get('gpa')}</p>")
                html_out.append("</div>")

        # Skills Section
        if skills:
            html_out.append(f"<h2>{self.STANDARD_SECTION_TITLES['skills']}</h2>")
            if isinstance(skills, list):
                if isinstance(skills[0], dict):
                    # Grouped skills
                    for group in skills:
                        category = group.get("category", "Technical Skills")
                        items = ", ".join(group.get("items", []))
                        html_out.append(f'<div class="skill-group"><strong>{category}:</strong> {items}</div>')
                else:
                    html_out.append(f"<p>{', '.join(skills)}</p>")

        # Projects Section
        if projects:
            html_out.append(f"<h2>{self.STANDARD_SECTION_TITLES['projects']}</h2>")
            for proj in projects:
                html_out.append('<div class="proj-item">')
                date_str = proj.get("date", "")
                html_out.append(
                    f'<div class="item-header"><span>{proj.get("title", "")}</span><span>{date_str}</span></div>'
                )
                if proj.get("technologies"):
                    techs = ", ".join(proj.get("technologies", []))
                    html_out.append(f'<div class="item-subheader"><span>Technologies: {techs}</span></div>')
                if proj.get("description"):
                    html_out.append(f"<p>{proj.get('description')}</p>")
                html_out.append("</div>")

        # Certifications
        if certifications:
            html_out.append(f"<h2>{self.STANDARD_SECTION_TITLES['certifications']}</h2>")
            html_out.append("<ul>")
            for cert in certifications:
                cert_text = f"<strong>{cert.get('name', '')}</strong> — {cert.get('issuer', '')} ({cert.get('issue_date', '')})"
                html_out.append(f"<li>{cert_text}</li>")
            html_out.append("</ul>")

        html_out.append("</body></html>")
        return "\n".join(html_out)


def get_template_instance(data: Optional[Dict[str, Any]] = None) -> ATSClassicTemplate:
    """Factory helper to instantiate ATS Classic Template."""
    return ATSClassicTemplate(data)
