"""
Job Description Parser Module (Person 2)

This module takes raw job description text and converts it into structured JSON
using an LLM, with light rule-based validation.

INPUT:
    jd_text (str) — raw job description text

OUTPUT:
    dict — structured job description data
"""

from backend.llm_client import call_llm
import json


# =========================================================
# SYSTEM PROMPT (LLM INSTRUCTION)
# =========================================================
SYSTEM_PROMPT = """
You are an expert job description parser.

Your task is to extract structured information from a job description.

Instructions:
1. Extract:
   - job_title
   - required_skills (must-have, essential)
   - preferred_skills (optional, nice-to-have)
   - role_keywords
   - responsibilities
   - experience (level, years, education)

2. Skill categories:
   - technical: tools, programming languages, frameworks (Python, SQL, AWS)
   - domain: knowledge areas (machine learning, data analytics)
   - soft: interpersonal skills (communication, teamwork)

3. Rules:
   - Only extract explicitly mentioned information
   - Do NOT hallucinate
   - Keep outputs concise
   - If information is missing, return null or empty list

4. Return ONLY valid JSON in the following format:

{
    "job_title": str,
    "required_skills": [
        {"name": str, "category": "technical" | "domain" | "soft"}
    ],
    "preferred_skills": [
        {"name": str, "category": "technical" | "domain" | "soft"}
    ],
    "role_keywords": [str],
    "responsibilities": [str],
    "experience": {
        "level": "entry" | "junior" | "mid" | "senior" | "not_specified",
        "years_min": int | null,
        "years_max": int | null,
        "education": str | null
    }
}

Do not include any explanation or extra text.
"""


# =========================================================
# RULE-BASED CLEANING (POST-PROCESSING)
# =========================================================
def _deduplicate_skills(skills):
    """Remove duplicate skills based on name."""
    seen = set()
    cleaned = []

    for s in skills:
        name = s.get("name", "").strip().lower()
        if name and name not in seen:
            seen.add(name)
            cleaned.append(s)

    return cleaned


def _clean_output(data):
    """Apply rule-based validation and cleaning."""
    if not isinstance(data, dict):
        return {"error": "Output is not a valid dictionary", "raw": data}

    # Deduplicate skills
    if "required_skills" in data:
        data["required_skills"] = _deduplicate_skills(data["required_skills"])

    if "preferred_skills" in data:
        data["preferred_skills"] = _deduplicate_skills(data["preferred_skills"])

    # Ensure keys exist (avoid downstream crash)
    data.setdefault("job_title", None)
    data.setdefault("required_skills", [])
    data.setdefault("preferred_skills", [])
    data.setdefault("role_keywords", [])
    data.setdefault("responsibilities", [])

    if "experience" not in data or not isinstance(data["experience"], dict):
        data["experience"] = {
            "level": "not_specified",
            "years_min": None,
            "years_max": None,
            "education": None
        }

    return data


# =========================================================
# MAIN FUNCTION
# =========================================================
def parse_jd(jd_text: str):
    """
    Parse a job description into structured JSON.

    Args:
        jd_text (str): Raw job description text

    Returns:
        dict: Structured job description data
    """

    # Step 1: Call LLM
    raw_output = call_llm(SYSTEM_PROMPT, jd_text)

    # Step 2: Convert JSON string → dict
    try:
        parsed_output = json.loads(raw_output)
    except Exception:
        return {
            "error": "Invalid JSON returned from LLM",
            "raw_output": raw_output
        }

    # Step 3: Rule-based cleaning
    cleaned_output = _clean_output(parsed_output)

    return cleaned_output