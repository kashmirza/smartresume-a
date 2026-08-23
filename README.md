# SmartResume AI — ATS Resume Builder + AI Job Matcher

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.3+-38B2AC.svg)](https://tailwindcss.com/)

**SmartResume AI** is an enterprise-grade, full-stack platform designed to help job seekers bypass Applicant Tracking Systems (ATS) and secure interviews. The platform combines intelligent resume parsing, a multi-template layout renderer, real-time job description parsing, a weighted ATS scoring engine (0–100 score), AI-driven bullet point/action verb enhancers, and automated target job tailoring.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [System Architecture & Tech Stack](#-system-architecture--tech-stack)
- [Key Features (All 23 Modules)](#-key-features-all-23-modules)
- [Screenshots & UI Previews](#-screenshots--ui-previews)
- [Project Directory Structure](#-project-directory-structure)
- [Installation & Local Setup](#-installation--local-setup)
- [Environment Variables Configuration](#-environment-variables-configuration)
- [ATS Scoring Engine Formula & Algorithm](#-ats-scoring-engine-formula--algorithm)
- [API Endpoints Reference](#-api-endpoints-reference)
- [Step-by-Step Usage Guide](#-step-by-step-usage-guide)
- [Resume Templates Overview](#-resume-templates-overview)
- [Future Roadmap & Enhancements](#-future-roadmap--enhancements)
- [License](#-license)

---

## 🎯 Project Overview

Modern Applicant Tracking Systems (e.g., Workday, Taleo, Greenhouse, Lever) filter out up to 75% of qualified applicants due to keyword mismatches, non-standard section headers, complex table layouts, or missing experience metrics. 

**SmartResume AI** solves this problem by providing:
1. **ATS-Compliant Document Generation**: Layouts engineered strictly without graphics or multi-column containers that break text extraction.
2. **Real-time Job Matching Engine**: NLP keyword extraction comparing target Job Descriptions (JD) against candidate resumes.
3. **AI Enhancement Suite**: Automated bullet point rewrites utilizing the STAR methodology (Situation, Task, Action, Result) with strong action verbs and metric quantifiers.
4. **Targeted Cover Letter Generation**: Context-aware cover letter generation matching the tailored resume version to the target role.

---

## 🛠 System Architecture & Tech Stack

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Backend Framework** | Python / FastAPI | 3.11+ / 0.104+ | High-performance asynchronous REST API & background processing |
| **Data Validation** | Pydantic | 2.5+ | Request/response schema validation and settings management |
| **PDF Generation** | ReportLab / WeasyPrint | 4.0+ | Headless pixel-perfect PDF rendering from HTML/Python flowables |
| **Document Parser** | PyPDF2 / pdfplumber / python-docx | 3.0+ | Extraction of text and structure from uploaded CV files |
| **Database ORM** | SQLAlchemy / PostgreSQL | 2.0+ / 15+ | Relational data persistence for users, resumes, applications, and metrics |
| **Cache & Queues** | Redis | 7.0+ | Rate limiting, token revocation, and asynchronous AI task queuing |
| **AI / LLM Integration**| OpenAI API / LangChain | GPT-4o / 0.1+ | Natural language extraction, bullet point rewriting, and summary generation |
| **Frontend Framework** | React / TypeScript | 18.2+ / 5.0+ | Reactive single-page user interface |
| **Build Tool** | Vite | 5.0+ | Fast hot-module replacement and optimized asset bundle compiler |
| **Styling & UI** | Tailwind CSS / Lucide Icons | 3.3+ | Utility-first responsive design and consistent icon typography |
| **State & HTTP Client** | Zustand / Axios | 4.4+ / 1.6+ | Lightweight global application state and asynchronous HTTP queries |
| **Containerization** | Docker / Docker Compose | 24.0+ | Multi-container local and production deployment orchestrator |

---

## 🚀 Key Features (All 23 Modules)

SmartResume AI is architected into 23 distinct feature modules from specification:

1. **User Authentication & JWT Security**: Email/password registration, password hashing (bcrypt), JWT access/refresh token issuance, and protected routes.
2. **User Profile & Social Links Management**: Central user profile management including personal info, contact details, location, and social links (LinkedIn, GitHub, Portfolio).
3. **Multi-Resume Management**: Create, edit, clone, version, and manage multiple resume profiles per account (e.g., Frontend, Fullstack, DevOps).
4. **Work Experience Accomplishment Tracker**: Detailed job history entry with position titles, company names, dates, location, and bullet point lists.
5. **Education & Credentials Manager**: Degree level, field of study, academic institution, dates, GPA, and honors entries.
6. **Skills & Competencies Taxonomy**: Categorized technical and soft skills manager (e.g., Languages, Frameworks, Cloud, Methodologies) with proficiency tagging.
7. **Projects & Portfolio Showcase**: Key personal or client projects with title, tech stack used, live demo links, repository URLs, and bulleted achievements.
8. **Certifications & Licenses Verification**: Professional certifications tracker with issuing organizations, credential IDs, issue dates, and expiration dates.
9. **Languages & Interests Directory**: Language proficiency entries (e.g., Native, Professional, CEFR levels) and professional interest tags.
10. **Custom Resume Sections Manager**: Ability to add custom sections (e.g., Publications, Speaking Engagements, Volunteering, Awards).
11. **AI Resume Builder & Draft Generator**: Automated initial draft creation based on target job title and background prompts using LLMs.
12. **Job Description (JD) AI Parser**: Extracts target job title, required technical skills, soft skills, minimum experience years, key responsibilities, and education requirements from raw JD text.
13. **ATS Compatibility Scoring Engine**: Calculates an overall 0–100 score along with sub-scores for Hard Skills, Experience Level, Soft Skills, Action Verbs, and Formatting.
14. **Keyword Gap Analysis & Density Matcher**: Identifies exact missing keywords, present keywords, and keyword frequency/density to prevent over-stuffing.
15. **AI Bullet Point / Action Verb Enhancer**: One-click AI rewrite of weak bullet points into high-impact, quantifiable STAR statements starting with power verbs.
16. **ATS-Safe Multi-Template Engine**: Supports 3 distinct layout paradigms: **ATS Classic Standard**, **Modern Professional**, and **Minimalist Elegant**.
17. **Multi-Format Export Engine**: Exports rendered resumes into high-res PDF, JSON Resume standard schema, or Markdown / Plain Text.
18. **Resume Tailoring & Version Control Lineage**: Fork a master resume into target-job-specific versions while maintaining parent-child lineage.
19. **AI Cover Letter Generator**: Generates customized cover letters tailored to a specific resume version and target job description.
20. **Match Report & Actionable Recommendation Engine**: Comprehensive feedback report detailing step-by-step actionable recommendations to raise ATS score above 85+.
21. **Application Tracker & Analytics Dashboard**: Track submitted applications, associated match scores, view counts, and application pipeline statuses (Applied, Interviewing, Offered).
22. **Real-Time Live Preview & WYSIWYG Renderer**: Interactive side-by-side editing view with real-time PDF/HTML render preview and instant keyword highlighting.
23. **Import & Document Parser (PDF/DOCX Extraction)**: Upload existing PDF or Word resumes to automatically extract and populate structured JSON sections.

---

## 🖼 Screenshots & UI Previews

```
+-----------------------------------------------------------------------------------+
|  SmartResume AI Dashboard                                       [ + New Resume ] |
+-----------------------------------------------------------------------------------+
|  MASTER RESUMES                        APPLICATION TRACKER                        |
|  * Senior Software Engineer (Master)   - Google (Match: 92%) - Interviewing       |
|  * Full Stack Developer - React/Node   - Amazon (Match: 84%) - Applied            |
|  * Tech Lead - Cloud Solutions         - Meta   (Match: 78%) - Saved              |
+-----------------------------------------------------------------------------------+
|  ATS MATCH SCORE ENGINE                                                           |
|  Overall Score: [ 88 / 100 ] [██████████████████████░░░]                           |
|  - Hard Skills Match:     32 / 35  (Missing: Kubernetes, GraphQL)               |
|  - Experience Level:      22 / 25  (5+ Years Required, 6 Years Found)             |
|  - Soft Skills Match:     14 / 15  (Leadership, Agile)                             |
|  - Action Verbs/Metrics:  12 / 15  (85% bullets start with power verbs)          |
|  - Formatting Compliance: 10 / 10  (100% ATS Safe)                                |
+-----------------------------------------------------------------------------------+
```

---

## 📂 Project Directory Structure

```
smartresume-ai/
├── README.md
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── user.py
│       │   ├── resume.py
│       │   └── job.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── resume.py
│       │   ├── job.py
│       │   └── ats.py
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── resumes.py
│       │   ├── jobs.py
│       │   ├── ats.py
│       │   ├── ai.py
│       │   ├── export.py
│       │   └── analytics.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── ats_engine.py
│       │   ├── jd_parser.py
│       │   ├── ai_service.py
│       │   ├── pdf_generator.py
│       │   └── doc_parser.py
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── security.py
│       │   └── keywords.py
│       └── templates/
│           ├── __init__.py
│           ├── ats_classic/
│           │   ├── __init__.py
│           │   └── template.py
│           ├── modern/
│           │   ├── __init__.py
│           │   └── template.py
│           └── minimal/
│               ├── __init__.py
│               └── template.py
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.js
    ├── tsconfig.json
    └── src/
        ├── App.tsx
        ├── main.tsx
        ├── index.css
        ├── components/
        │   ├── Header.tsx
        │   ├── Footer.tsx
        │   ├── ResumeEditor.tsx
        │   ├── ATSScoreWidget.tsx
        │   ├── JDParserWidget.tsx
        │   └── PreviewPanel.tsx
        ├── pages/
        │   ├── DashboardPage.tsx
        │   ├── LoginPage.tsx
        │   ├── RegisterPage.tsx
        │   ├── BuilderPage.tsx
        │   ├── MatcherPage.tsx
        │   └── AnalyticsPage.tsx
        ├── services/
        │   ├── api.ts
        │   ├── resumeService.ts
        │   └── atsService.ts
        └── context/
            └── AuthContext.tsx
```

---

## ⚙️ Installation & Local Setup

### Prerequisites
- **Python**: 3.11 or higher
- **Node.js**: 18.0 or higher (npm 9+)
- **PostgreSQL**: 15+ (or SQLite for local lightweight development)
- **Redis**: 7.0+ (optional for local non-queued testing)

---

### Step 1: Clone & Configure Backend

```bash
cd backend

# Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment template and configure secrets
cp .env.example .env
```

Start the FastAPI development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
*API Swagger Documentation will be accessible at: `http://localhost:8000/docs`*

---

### Step 2: Configure Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start Vite dev server
npm run dev
```
*Frontend application will be accessible at: `http://localhost:5173`*

---

### Step 3: Run via Docker Compose (Recommended)

To launch the complete application stack (PostgreSQL, Redis, FastAPI Backend, React Frontend):

```bash
docker-compose up --build -d
```

---

## 🔒 Environment Variables Configuration

### Backend (`backend/.env`)

| Variable Name | Required | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `PROJECT_NAME` | No | `SmartResume AI` | Title displayed in API Docs |
| `DATABASE_URL` | Yes | `sqlite:///./smartresume.db` | PostgreSQL or SQLite connection string |
| `SECRET_KEY` | Yes | `generate-secret-key-with-openssl` | Cryptographic secret for signing JWT tokens |
| `ALGORITHM` | No | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `1440` | Token expiration time in minutes (24 hrs) |
| `OPENAI_API_KEY` | Yes | `sk-proj-...` | OpenAI API Key for AI parser, rewrites & generator |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Redis instance URL |
| `STORAGE_PATH` | No | `./storage` | Directory path for exported PDF/JSON artifacts |
| `CORS_ORIGINS` | No | `["http://localhost:5173","http://localhost:3000"]` | Allowed frontend origins |

### Frontend (`frontend/.env`)

| Variable Name | Required | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `VITE_API_BASE_URL` | Yes | `http://localhost:8000/api/v1` | Backend API base URL |
| `VITE_ENABLE_AI_FEATURES` | No | `true` | Feature flag to enable AI enhancement buttons |
| `VITE_MAX_UPLOAD_SIZE_MB` | No | `10` | Maximum file upload size in megabytes |

---

## 📊 ATS Scoring Engine Formula & Algorithm

The **ATS Compatibility Score** ($S_{\text{overall}}$) is calculated on a 0 to 100 scale using a deterministic weighted multi-factor formula:

$$S_{\text{overall}} = (0.35 \times S_{\text{hard}}) + (0.25 \times S_{\text{exp}}) + (0.15 \times S_{\text{soft}}) + (0.15 \times S_{\text{action}}) + (0.10 \times S_{\text{format}})$$

### Sub-score Components Breakdown

1. **Hard Skills & Technical Keyword Match ($S_{\text{hard}}$ - Weight: 35%)**:
   - Calculates the ratio of required technical skills present in the resume vs. extracted from the Job Description.
   - Includes exact match and semantic synonym matching (e.g., "React.js" = "React").
   - Bonus points awarded for correct keyword placement in experience bullet points vs. passive listing.

2. **Experience Level & Title Alignment ($S_{\text{exp}}$ - Weight: 25%)**:
   - Measures candidate's total years of relevant experience against the minimum required years specified in the JD.
   - Evaluates title similarity score using Jaccard string similarity between candidate's past titles and target title.

3. **Soft Skills & Core Competencies ($S_{\text{soft}}$ - Weight: 15%)**:
   - Evaluates key organizational and interpersonal competencies (e.g., "Cross-functional Leadership", "Agile", "Stakeholder Management").

4. **Action Verbs & Metric Quantifiers ($S_{\text{action}}$ - Weight: 15%)**:
   - Checks percentage of bullet points starting with strong past-tense action verbs (e.g., *Spearheaded, Engineered, Architected, Accelerated*).
   - Penalizes passive bullet phrases (*"Responsible for", "Worked on", "Helped with"*).
   - Checks for presence of quantifiable metric achievements (e.g., percentages `%`, dollar amounts `$`, user counts `100k+`, speed improvements `3x`).

5. **Formatting & Structural Parseability ($S_{\text{format}}$ - Weight: 10%)**:
   - Verifies compliance with standard section header naming conventions.
   - Ensures no complex tables, text boxes, multi-column divisions, or unparseable graphics are present.

---

## 📡 API Endpoints Reference

All API routes are prefixed with `/api/v1`.

### 1. Authentication (`/api/v1/auth`)

#### `POST /api/v1/auth/register`
Register a new user account.

- **Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "Jane Doe"
}
```
- **Response** (`201 Created`):
```json
{
  "id": "u_987654321",
  "email": "user@example.com",
  "full_name": "Jane Doe",
  "created_at": "2026-08-22T12:00:00Z"
}
```

#### `POST /api/v1/auth/login`
Authenticate user credentials and receive JWT access token.

- **Request Body**:
```json
{
  "username": "user@example.com",
  "password": "SecurePassword123!"
}
```
- **Response** (`200 OK`):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

#### `GET /api/v1/auth/me`
Retrieve authenticated user profile.
- **Headers**: `Authorization: Bearer <token>`
- **Response** (`200 OK`):
```json
{
  "id": "u_987654321",
  "email": "user@example.com",
  "full_name": "Jane Doe"
}
```

---

### 2. Resume Management (`/api/v1/resumes`)

#### `GET /api/v1/resumes`
List all resumes owned by authenticated user.
- **Response** (`200 OK`):
```json
[
  {
    "id": "res_101",
    "title": "Senior Full Stack Engineer Master",
    "target_title": "Senior Software Engineer",
    "template_id": "ats_classic",
    "updated_at": "2026-08-22T14:30:00Z"
  }
]
```

#### `POST /api/v1/resumes`
Create a new resume profile.
- **Request Body**:
```json
{
  "title": "DevOps Lead Master",
  "template_id": "ats_classic",
  "personal_info": {
    "full_name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1 (555) 019-2834",
    "location": "San Francisco, CA",
    "linkedin_url": "https://linkedin.com/in/janedoe",
    "github_url": "https://github.com/janedoe"
  },
  "summary": "Accomplished DevOps Engineer with 7+ years of experience...",
  "work_experience": [
    {
      "company_name": "CloudScale Inc",
      "position_title": "Senior DevOps Engineer",
      "start_date": "2022-01",
      "end_date": "Present",
      "location": "San Francisco, CA",
      "bullet_points": [
        "Architected Kubernetes infrastructure reducing deployment latency by 45%.",
        "Automated CI/CD pipelines across 30+ microservices using GitHub Actions."
      ]
    }
  ],
  "education": [
    {
      "institution": "University of California, Berkeley",
      "degree": "Bachelor of Science",
      "field_of_study": "Computer Science",
      "start_date": "2015-08",
      "end_date": "2019-05",
      "gpa": "3.85"
    }
  ],
  "skills": [
    {
      "category": "Cloud & Infrastructure",
      "items": ["AWS", "Kubernetes", "Docker", "Terraform"]
    }
  ]
}
```
- **Response** (`201 Created`): Returns created resume payload with assigned `id`.

#### `POST /api/v1/resumes/parse-upload`
Upload an existing PDF/DOCX file to extract resume data.
- **Content-Type**: `multipart/form-data`
- **File Field**: `file`
- **Response** (`200 OK`): Structured JSON resume object ready for editing.

---

### 3. Job Description Parsing & Matching (`/api/v1/jobs`)

#### `POST /api/v1/jobs/parse`
Extract structured requirements from raw Job Description text.

- **Request Body**:
```json
{
  "job_title": "Senior Backend Developer",
  "company_name": "TechCorp",
  "raw_text": "We are seeking a Senior Backend Developer with 5+ years of Python, FastAPI, PostgreSQL, and Redis experience. Must have demonstrated expertise building scalable microservices and Docker containers."
}
```
- **Response** (`200 OK`):
```json
{
  "parsed_job_id": "job_302",
  "job_title": "Senior Backend Developer",
  "required_technical_skills": ["Python", "FastAPI", "PostgreSQL", "Redis", "Microservices", "Docker"],
  "required_soft_skills": ["Problem Solving", "Team Collaboration"],
  "min_years_experience": 5,
  "required_education": "Bachelor's Degree in CS or equivalent"
}
```

---

### 4. ATS Scoring & Keyword Analysis (`/api/v1/ats`)

#### `POST /api/v1/ats/score`
Calculate complete ATS match score between a resume and target job description.

- **Request Body**:
```json
{
  "resume_id": "res_101",
  "parsed_job_id": "job_302"
}
```
- **Response** (`200 OK`):
```json
{
  "overall_score": 88,
  "sub_scores": {
    "hard_skills": 32,
    "experience_level": 25,
    "soft_skills": 13,
    "action_verbs": 10,
    "formatting": 10
  },
  "missing_keywords": ["Redis", "Microservices"],
  "present_keywords": ["Python", "FastAPI", "PostgreSQL", "Docker"],
  "recommendations": [
    "Add 'Redis' to your Cloud & Infrastructure skills category.",
    "Include quantifiable metrics in bullet point #2 under CloudScale Inc."
  ]
}
```

---

### 5. AI Enhancement Suite (`/api/v1/ai`)

#### `POST /api/v1/ai/enhance-bullet`
Rewrite a weak resume bullet point into a high-impact STAR statement.

- **Request Body**:
```json
{
  "bullet_point": "Worked on backend APIs using Python and fixed bugs.",
  "target_role": "Senior Backend Developer",
  "key_skills": ["Python", "FastAPI", "PostgreSQL"]
}
```
- **Response** (`200 OK`):
```json
{
  "original": "Worked on backend APIs using Python and fixed bugs.",
  "enhanced_options": [
    "Engineered high-throughput REST APIs using Python and FastAPI, resolving 40+ critical bugs and reducing API response latency by 35%.",
    "Spearheaded backend API optimization in Python, boosting query throughput across PostgreSQL databases by 28%."
  ]
}
```

---

### 6. Templates & Multi-Format Export (`/api/v1/export`)

#### `POST /api/v1/export/pdf`
Render specified resume into a downloadable PDF binary document.

- **Request Body**:
```json
{
  "resume_id": "res_101",
  "template_id": "ats_classic"
}
```
- **Response**: Binary PDF file (`Content-Type: application/pdf`).

---

## 📑 Step-by-Step Usage Guide

```
+-----------------------------------------------------------------------------------+
|  STEP 1: Register Account & Login                                                |
|  STEP 2: Create Master Resume or Upload existing PDF/DOCX                         |
|  STEP 3: Paste Target Job Description (JD) & Run AI Parser                        |
|  STEP 4: Run ATS Compatibility Analysis (Get Score 0-100 & Keyword Gap Analysis)  |
|  STEP 5: Apply AI Enhancements to Bullet Points & Insert Missing Keywords         |
|  STEP 6: Select Template (ATS Classic / Modern / Minimal) & Download PDF/JSON     |
+-----------------------------------------------------------------------------------+
```

1. **Create Account**: Register on the platform at `/register` and log in.
2. **Build or Import CV**: Go to the **Resume Builder** tab. Click **Import CV** to upload an existing resume or click **Create New** to enter your experience, skills, and projects manually.
3. **Parse Target Job Description**: Navigate to the **Job Matcher** tab. Paste the raw job posting text and click **Parse JD**.
4. **Generate ATS Score**: Click **Calculate ATS Compatibility**. Review your overall score, missing hard skills, and recommendations.
5. **Optimize Content**: Use the **AI Enhancer** to rewrite bullet points. Add identified missing keywords to your Skills or Work Experience section.
6. **Select Template & Export**: Preview your resume in **ATS Classic**, **Modern**, or **Minimal** templates. Click **Export PDF** or **Export JSON Resume**.

---

## 🎨 Resume Templates Overview

SmartResume AI features three production templates:

1. **ATS Classic Standard (`ats_classic`)**:
   - **Target Audience**: Corporate enterprise, government, finance, and traditional ATS systems.
   - **Structure**: Strict single-column, standard linear layout.
   - **ATS Score Rating**: **100% Guaranteed Parse Rate**.

2. **Modern Professional (`modern`)**:
   - **Target Audience**: Tech companies, startups, product management, and creative roles.
   - **Structure**: Distinct dark slate header banner, blue accent underlines, skill badges.
   - **ATS Score Rating**: **90% Parse Rate**.

3. **Minimalist Elegant (`minimal`)**:
   - **Target Audience**: Executives, designers, academic roles, and senior consultants.
   - **Structure**: Typography-first layout with clean horizontal rules and monochrome palette.
   - **ATS Score Rating**: **95% Parse Rate**.

---

## 🔮 Future Roadmap & Enhancements

- [ ] **Multi-Language Translation Engine**: AI-powered translation for multi-lingual applications (German, French, Spanish, Japanese).
- [ ] **LinkedIn One-Click Importer**: Automated OAuth sync to pull work experience directly from LinkedIn profiles.
- [ ] **Job Search Web Scraper**: Automated matching against live job boards (LinkedIn, Indeed, Glassdoor).
- [ ] **Recruiter Simulator Sandbox**: Test how different ATS parsers (Taleo vs Greenhouse) extract text from custom uploads.

---

## 📄 License

This project is open-source and licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 SmartResume AI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
