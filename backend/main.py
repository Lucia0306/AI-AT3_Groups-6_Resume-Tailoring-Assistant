from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import tempfile
import os
import json

from backend.file_extractors import extract_resume_text
from backend.modules.resume_parser import parse_resume
from backend.modules.jd_parsing import parse_jd
from backend.modules.tailored_resume_generator import generate_tailored_resume_json

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(
    jd_text: str = Form(...),
    resume_pdf: UploadFile = File(...)
):
    suffix = os.path.splitext(resume_pdf.filename)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await resume_pdf.read())
        temp_path = tmp.name

    try:
        # 1. Extract resume text from uploaded file
        resume_text = extract_resume_text(temp_path)

        # 2. Parse JD
        jd_parsed_dict = parse_jd(jd_text)
        jd_parsed_str = json.dumps(jd_parsed_dict)

        # 3. Parse resume
        resume_parsed_str = parse_resume(resume_text)

        # 4. Temporary placeholder alignment
        alignment_dict = {
            "matched": [],
            "missing": [],
            "weak_matches": []
        }
        alignment_str = json.dumps(alignment_dict)

        # 5. Generate tailored resume
        tailored_resume_str = generate_tailored_resume_json(
            jd_json=jd_parsed_str,
            resume_json=resume_parsed_str,
            alignment_json=alignment_str,
            use_api=False
        )

        return {
            "jd_parsed": jd_parsed_str,
            "resume_parsed": resume_parsed_str,
            "alignment": alignment_str,
            "tailored_resume": tailored_resume_str
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)