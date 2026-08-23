"""
SmartResume AI - Modern Professional Template Definition

This module provides layout definitions, styling rules, and rendering methods
for the Modern Professional template. Designed for contemporary corporate, technology,
and management roles where visual polish and clear hierarchy are paramount.

Key Characteristics:
- Clean two-column accent or top hero header design
- Primary accent color palette (Slate / Navy Blue `#1E293B` and `#2563EB`)
- Skill badges with visual category grouping
- Crisp modern typography (Roboto, Inter, Arial)
- Formatted bullet points with strong visual spacing
"""

from typing import Dict, Any, List, Optional


class ModernTemplate:
    """
    Modern Professional Resume Template renderer.
    Combines strong visual presentation with clean layout structure suitable for tech, design, and management.
    """

    TEMPLATE_ID = "modern"
    NAME = "Modern Professional"
    DESCRIPTION = "Contemporary professional layout featuring sleek header accents, skill badges, and clear visual hierarchy."
    AUTHOR = "SmartResume AI Team"
    VERSION = "1.0.0"

    CONFIG = {
        "page_size": "LETTER",
        "margin_top_inches": 0.6,
        "margin_bottom_inches": 0.6,
        "margin_left_inches": 0.6,
        "margin_right_inches": 0.6,
        "font_family": "Arial, sans-serif",
        "color_primary": "#1E293B",
        "color_accent": "#2563EB",
        "color_light_bg": "#F8FAFC",
        "color_text": "#334155",
        "font_size_name": 22,
        "font_size_title": 13,
        "font_size_heading": 12,
        "font_size_body": 10,
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
            "ats_compatibility_score": 90,
            "features": [
                "Modern Header Block with Accent Colors",
                "Skill Pill Badges",
                "Clean Section Dividers",
                "Optimized Whitespace",
            ],
            "config": self.CONFIG,
        }

    def render_html(self, data: Optional[Dict[str, Any]] = None) -> str:
        """Render resume data into Modern HTML layout."""
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
            "body { font-family: Arial, Helvetica, sans-serif; font-size: 10pt; color: #334155; margin: 0; padding: 0.5in; background: #fff; }",
            ".header-banner { background: #1E293B; color: #ffffff; padding: 20px; border-radius: 6px; margin-bottom: 20px; }",
            ".header-banner h1 { margin: 0 0 6px 0; font-size: 22pt; color: #ffffff; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }",
            ".header-banner .title { font-size: 12pt; color: #93C5FD; font-weight: 500; margin-bottom: 10px; }",
            ".contact-links { font-size: 9.5pt; color: #E2E8F0; display: flex; flex-wrap: wrap; gap: 12px; }",
            "h2 { font-size: 12pt; color: #1E293B; border-bottom: 2px solid #2563EB; padding-bottom: 4px; margin-top: 18px; margin-bottom: 10px; font-weight: 700; text-transform: uppercase; }",
            ".summary-box { background: #F8FAFC; border-left: 4px solid #2563EB; padding: 10px 14px; margin-bottom: 15px; border-radius: 0 4px 4px 0; }",
            ".exp-card, .edu-card, .proj-card { margin-bottom: 14px; }",
            ".card-header { display: flex; justify-content: space-between; align-items: baseline; font-weight: bold; color: #0F172A; }",
            ".card-sub { display: flex; justify-content: space-between; font-size: 9.5pt; color: #2563EB; font-weight: 600; margin-bottom: 4px; }",
            "ul { margin-top: 4px; padding-left: 18px; }",
            "li { margin-bottom: 3px; }",
            ".skills-container { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }",
            ".skill-badge { background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; padding: 3px 8px; border-radius: 4px; font-size: 9pt; font-weight: 500; }",
            "</style>",
            "</head>",
            "<body>",
        ]

        # Modern Header Banner
        html_out.append('<div class="header-banner">')
        html_out.append(f"<h1>{personal.get('full_name', '')}</h1>")
        if personal.get("target_title"):
            html_out.append(f'<div class="title">{personal.get("target_title")}</div>')

        contacts = []
        if personal.get("phone"):
            contacts.append(f"<span>📞 {personal.get('phone')}</span>")
        if personal.get("email"):
            contacts.append(f"<span>✉️ {personal.get('email')}</span>")
        if personal.get("location"):
            contacts.append(f"<span>📍 {personal.get('location')}</span>")
        if personal.get("linkedin_url"):
            contacts.append(f"<span>🔗 {personal.get('linkedin_url')}</span>")

        html_out.append(f'<div class="contact-links">{" | ".join(contacts)}</div>')
        html_out.append("</div>")  # End banner

        # Summary
        if summary:
            html_out.append(f"<h2>Professional Profile</h2>")
            html_out.append(f'<div class="summary-box">{summary}</div>')

        # Experience
        if experiences:
            html_out.append(f"<h2>Work Experience</h2>")
            for exp in experiences:
                html_out.append('<div class="exp-card">')
                date_str = f"{exp.get('start_date', '')} – {exp.get('end_date', 'Present')}"
                html_out.append(
                    f'<div class="card-header"><span>{exp.get("position_title", "")}</span><span>{date_str}</span></div>'
                )
                html_out.append(
                    f'<div class="card-sub"><span>{exp.get("company_name", "")} ({exp.get("location", "")})</span></div>'
                )
                bullets = exp.get("bullet_points", [])
                if bullets:
                    html_out.append("<ul>")
                    for bullet in bullets:
                        html_out.append(f"<li>{bullet}</li>")
                    html_out.append("</ul>")
                html_out.append("</div>")

        # Skills
        if skills:
            html_out.append("<h2>Key Competencies & Technical Skills</h2>")
            if isinstance(skills, list):
                if isinstance(skills[0], dict):
                    for group in skills:
                        html_out.append(f"<p><strong>{group.get('category', 'Skills')}:</strong></p>")
                        html_out.append('<div class="skills-container">')
                        for item in group.get("items", []):
                            html_out.append(f'<span class="skill-badge">{item}</span>')
                        html_out.append("</div>")
                else:
                    html_out.append('<div class="skills-container">')
                    for sk in skills:
                        html_out.append(f'<span class="skill-badge">{sk}</span>')
                    html_out.append("</div>")

        # Education
        if education:
            html_out.append("<h2>Education & Credentials</h2>")
            for edu in education:
                html_out.append('<div class="edu-card">')
                date_str = f"{edu.get('start_date', '')} – {edu.get('end_date', '')}"
                html_out.append(
                    f'<div class="card-header"><span>{edu.get("institution", "")}</span><span>{date_str}</span></div>'
                )
                html_out.append(
                    f'<div class="card-sub"><span>{edu.get("degree", "")} in {edu.get("field_of_study", "")}</span></div>'
                )
                html_out.append("</div>")

        # Projects
        if projects:
            html_out.append("<h2>Featured Projects</h2>")
            for proj in projects:
                html_out.append('<div class="proj-card">')
                html_out.append(
                    f'<div class="card-header"><span>{proj.get("title", "")}</span><span>{proj.get("date", "")}</span></div>'
                )
                if proj.get("description"):
                    html_out.append(f"<p>{proj.get('description')}</p>")
                html_out.append("</div>")

        html_out.append("</body></html>")
        return "\n".join(html_out)


def get_template_instance(data: Optional[Dict[str, Any]] = None) -> ModernTemplate:
    """Factory helper to instantiate Modern Template."""
    return ModernTemplate(data)
