"""
SmartResume AI - Minimalist Template Definition

This module provides layout definitions, styling rules, and rendering methods
for the Minimalist template. Designed for candidates seeking a refined, typography-first
resume design with generous whitespace and understated elegance.

Key Characteristics:
- Typography-focused single-column layout
- Monochromatic charcoal & soft gray palette (`#1A202C`, `#4A5568`)
- Subtle border lines and ample whitespace
- Compact header layout
- Clean, readable sans-serif or standard serif styling
"""

from typing import Dict, Any, List, Optional


class MinimalTemplate:
    """
    Minimalist Resume Template renderer.
    Delivers maximum legibility and elegance through clean spacing, typography, and minimal ornament.
    """

    TEMPLATE_ID = "minimal"
    NAME = "Minimalist Elegant"
    DESCRIPTION = "Sleek, typography-focused design with generous whitespace and refined structural dividers."
    AUTHOR = "SmartResume AI Team"
    VERSION = "1.0.0"

    CONFIG = {
        "page_size": "LETTER",
        "margin_top_inches": 0.75,
        "margin_bottom_inches": 0.75,
        "margin_left_inches": 0.75,
        "margin_right_inches": 0.75,
        "font_family": "Georgia, serif",
        "color_primary": "#1A202C",
        "color_secondary": "#4A5568",
        "color_border": "#E2E8F0",
        "font_size_name": 20,
        "font_size_heading": 11,
        "font_size_body": 9.5,
    }

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self.data = data or {}

    def get_metadata(self) -> Dict[str, Any]:
        """Return template metadata."""
        return {
            "template_id": self.TEMPLATE_ID,
            "name": self.NAME,
            "description": self.DESCRIPTION,
            "version": self.VERSION,
            "ats_compatibility_score": 95,
            "features": [
                "Typography-focused design",
                "Monochrome charcoal theme",
                "Clean thin line dividers",
                "Spacious layout",
            ],
            "config": self.CONFIG,
        }

    def render_html(self, data: Optional[Dict[str, Any]] = None) -> str:
        """Render resume data into Minimalist HTML format."""
        resume = data or self.data
        personal = resume.get("personal_info", {})
        summary = resume.get("summary", "")
        experiences = resume.get("work_experience", [])
        education = resume.get("education", [])
        skills = resume.get("skills", [])
        projects = resume.get("projects", [])
        certifications = resume.get("certifications", [])

        html_out = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            '<meta charset="utf-8"/>',
            f"<title>{personal.get('full_name', 'Resume')}</title>",
            "<style>",
            "body { font-family: Georgia, serif; font-size: 9.5pt; color: #2D3748; margin: 0.75in; line-height: 1.4; }",
            ".header { text-align: left; border-bottom: 1px solid #CBD5E0; padding-bottom: 12px; margin-bottom: 16px; }",
            ".header h1 { font-size: 20pt; color: #1A202C; margin: 0 0 4px 0; font-weight: normal; letter-spacing: 0.5px; }",
            ".header .sub-contact { font-size: 9pt; color: #718096; text-transform: uppercase; letter-spacing: 1px; }",
            "h2 { font-size: 10.5pt; font-family: Helvetica, Arial, sans-serif; text-transform: uppercase; letter-spacing: 1.5px; color: #4A5568; margin-top: 18px; margin-bottom: 8px; border-bottom: 1px solid #E2E8F0; padding-bottom: 2px; }",
            ".section-block { margin-bottom: 14px; }",
            ".row-header { display: flex; justify-content: space-between; font-weight: bold; color: #1A202C; }",
            ".row-sub { display: flex; justify-content: space-between; font-style: italic; color: #718096; margin-bottom: 4px; }",
            "ul { margin-top: 4px; padding-left: 16px; list-style-type: circle; }",
            "li { margin-bottom: 3px; }",
            ".skills-list { font-family: Helvetica, Arial, sans-serif; font-size: 9pt; color: #4A5568; }",
            "</style>",
            "</head>",
            "<body>",
        ]

        # Minimal Header
        html_out.append('<div class="header">')
        html_out.append(f"<h1>{personal.get('full_name', '')}</h1>")
        c_parts = []
        if personal.get("email"):
            c_parts.append(personal.get("email"))
        if personal.get("phone"):
            c_parts.append(personal.get("phone"))
        if personal.get("location"):
            c_parts.append(personal.get("location"))
        if personal.get("linkedin_url"):
            c_parts.append(personal.get("linkedin_url"))

        html_out.append(f'<div class="sub-contact">{" • ".join(c_parts)}</div>')
        html_out.append("</div>")

        # Summary
        if summary:
            html_out.append("<h2>Profile</h2>")
            html_out.append(f'<div class="section-block"><p>{summary}</p></div>')

        # Experience
        if experiences:
            html_out.append("<h2>Experience</h2>")
            for exp in experiences:
                html_out.append('<div class="section-block">')
                date_str = f"{exp.get('start_date', '')} — {exp.get('end_date', 'Present')}"
                html_out.append(
                    f'<div class="row-header"><span>{exp.get("position_title", "")}</span><span>{date_str}</span></div>'
                )
                html_out.append(
                    f'<div class="row-sub"><span>{exp.get("company_name", "")}, {exp.get("location", "")}</span></div>'
                )
                bullets = exp.get("bullet_points", [])
                if bullets:
                    html_out.append("<ul>")
                    for b in bullets:
                        html_out.append(f"<li>{b}</li>")
                    html_out.append("</ul>")
                html_out.append("</div>")

        # Education
        if education:
            html_out.append("<h2>Education</h2>")
            for edu in education:
                html_out.append('<div class="section-block">')
                date_str = f"{edu.get('start_date', '')} — {edu.get('end_date', '')}"
                html_out.append(
                    f'<div class="row-header"><span>{edu.get("institution", "")}</span><span>{date_str}</span></div>'
                )
                html_out.append(
                    f'<div class="row-sub"><span>{edu.get("degree", "")} in {edu.get("field_of_study", "")}</span></div>'
                )
                html_out.append("</div>")

        # Skills
        if skills:
            html_out.append("<h2>Skills</h2>")
            html_out.append('<div class="section-block skills-list">')
            if isinstance(skills, list):
                if isinstance(skills[0], dict):
                    for group in skills:
                        html_out.append(
                            f"<p><strong>{group.get('category', 'Skills')}:</strong> {', '.join(group.get('items', []))}</p>"
                        )
                else:
                    html_out.append(f"<p>{' • '.join(skills)}</p>")
            html_out.append("</div>")

        # Projects
        if projects:
            html_out.append("<h2>Projects</h2>")
            for proj in projects:
                html_out.append('<div class="section-block">')
                html_out.append(
                    f'<div class="row-header"><span>{proj.get("title", "")}</span><span>{proj.get("date", "")}</span></div>'
                )
                if proj.get("description"):
                    html_out.append(f"<p>{proj.get('description')}</p>")
                html_out.append("</div>")

        html_out.append("</body></html>")
        return "\n".join(html_out)


def get_template_instance(data: Optional[Dict[str, Any]] = None) -> MinimalTemplate:
    """Factory helper to instantiate Minimal Template."""
    return MinimalTemplate(data)
