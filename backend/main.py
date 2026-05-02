from fastapi import FastAPI, UploadFile, File, Form
import json

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(
    jd_text: str = Form(...),
    resume_pdf: UploadFile = File(...)
):
    mock_jd = {
        "job_title": "Graduate Data Analyst",
        "required_skills": [
            {"name": "python", "category": "technical"},
            {"name": "sql", "category": "technical"},
            {"name": "data analysis", "category": "domain"},
            {"name": "communication", "category": "soft"}
        ],
        "preferred_skills": [
            {"name": "tableau", "category": "technical"},
            {"name": "power bi", "category": "technical"}
        ],
        "role_keywords": ["dashboard", "reporting", "insights"],
        "responsibilities": [
            "Analyse structured datasets",
            "Build dashboards",
            "Communicate findings to stakeholders"
        ],
        "experience": {
            "level": "entry",
            "years_min": 0,
            "years_max": 2,
            "education": "Bachelor or Master degree"
        }
    }

    mock_resume = {
        "candidate_name": "Jordan Chen",
        "skills": [
            {"name": "Python", "category": "technical"},
            {"name": "SQL", "category": "technical"},
            {"name": "Tableau", "category": "technical"},
            {"name": "Data Analysis", "category": "domain"},
            {"name": "Communication", "category": "soft"}
        ],
        "education": [
            {
                "degree": "Master of Commerce",
                "institution": "The University of Sydney",
                "graduation_year": 2026,
                "gpa": None,
                "relevant_coursework": ["Data Analytics", "Business Intelligence"]
            }
        ],
        "work_experience": [
            {
                "company": "ABC Company",
                "title": "Data Intern",
                "start_date": "2024-06",
                "end_date": "2024-08",
                "bullets": [
                    {
                        "text": "Prepared summary tables and charts for weekly reporting.",
                        "skills_mentioned": ["Python", "Data Analysis"]
                    },
                    {
                        "text": "Cleaned and organised internal datasets for team use.",
                        "skills_mentioned": ["SQL", "Data Analysis"]
                    }
                ]
            }
        ],
        "projects": [
            {
                "name": "Sales Dashboard Project",
                "technologies": ["Tableau", "SQL"],
                "bullets": [
                    {
                        "text": "Built a Tableau dashboard to visualise monthly sales trends.",
                        "skills_mentioned": ["Tableau", "SQL"]
                    }
                ]
            }
        ]
    }

    mock_alignment = {
        "matched": [
            {"item": "python", "source": "required_skills"},
            {"item": "sql", "source": "required_skills"},
            {"item": "communication", "source": "required_skills"}
        ],
        "missing": [
            {"item": "power bi", "source": "preferred_skills", "importance": "medium"}
        ],
        "weak_matches": [
            {
                "jd_requirement": "Communicate findings to stakeholders",
                "resume_bullet": "Prepared summary tables and charts for weekly reporting.",
                "reason": "The evidence is relevant but could be expressed more clearly for communication impact."
            },
            {
                "jd_requirement": "Build dashboards",
                "resume_bullet": "Built a Tableau dashboard to visualise monthly sales trends.",
                "reason": "The dashboard experience is relevant and can be tailored more directly to the JD wording."
            }
        ]
    }

    mock_tailored_resume = {
        "professional_summary": (
            "Data-focused graduate candidate with experience in Python, SQL, Tableau, and data analysis. "
            "Demonstrated ability to support reporting, dashboard development, and insight communication through academic and practical work. "
            "Interested in entry-level data analyst roles involving structured datasets, dashboards, and stakeholder-facing analysis."
        ),
        "reordered_skills": [
            "Python",
            "SQL",
            "Data Analysis",
            "Communication",
            "Tableau"
        ],
        "rewritten_bullets": [
            {
                "original": "Prepared summary tables and charts for weekly reporting.",
                "revised": "Prepared summary tables and charts to support weekly reporting and communicate insights clearly to internal stakeholders.",
                "rationale": "Reframed the bullet to emphasise communication and reporting relevance."
            },
            {
                "original": "Built a Tableau dashboard to visualise monthly sales trends.",
                "revised": "Built a Tableau dashboard to visualise monthly sales trends and support dashboard-based reporting.",
                "rationale": "Aligned the wording more directly with the dashboard requirement."
            }
        ],
        "full_resume_text": """Jordan Chen

Email: jordan.chen@email.com | Phone: 0400 000 000 | Sydney, Australia

Professional Summary
Data-focused graduate candidate with experience in Python, SQL, Tableau, and data analysis. Demonstrated ability to support reporting, dashboard development, and insight communication through academic and practical work. Interested in entry-level data analyst roles involving structured datasets, dashboards, and stakeholder-facing analysis.

Skills
Python | SQL | Data Analysis | Communication | Tableau

Education
Master of Commerce, The University of Sydney, 2026

Work Experience
Data Intern, ABC Company
- Prepared summary tables and charts to support weekly reporting and communicate insights clearly to internal stakeholders.
- Cleaned and organised internal datasets for team use.

Projects
Sales Dashboard Project
- Built a Tableau dashboard to visualise monthly sales trends and support dashboard-based reporting.
"""
    }

    return {
        "jd_parsed": json.dumps(mock_jd),
        "resume_parsed": json.dumps(mock_resume),
        "alignment": json.dumps(mock_alignment),
        "tailored_resume": json.dumps(mock_tailored_resume)
    }