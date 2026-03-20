"""
Gemini-powered fax classifier.

Sends the raw PDF bytes to Gemini Flash and returns a classification
and patient info as a dict. Used as a second opinion alongside the
keyword-based classifier in modules/fax_classifier.py.
"""

import json
import os
import sys

from dateutil import parser as dateparser
from google import genai
from google.genai import types

GEMINI_MODEL = "gemini-2.0-flash"

VALID_CATEGORIES = {
    "result - routine",
    "result - urgent",
    "scheduling",
    "insurance",
    "other",
}

_ERROR_DICT: dict = {
    "gemini_category": "error",
    "gemini_patient_name": "",
    "gemini_patient_dob": "",
}

_PROMPT = """\
You are a medical document classifier. Analyze this fax and return a JSON object
with exactly these three fields:

{
  "category": <one of: "result - routine", "result - urgent", "scheduling", "insurance", "other">,
  "patient_name": <full name as a string, or "" if not found>,
  "patient_dob": <date of birth in YYYY-MM-DD format, or "" if not found>
}

Classification rules:
- "result - routine": diagnostic imaging or lab report with no urgent/critical findings
- "result - urgent": diagnostic imaging or lab report with urgent or critical findings
- "scheduling": notification that a patient has not yet scheduled an exam
- "insurance": prior authorization request or insurance-related communication
- "other": anything that does not fit the above categories

Return only the JSON object. No explanation, no markdown, no extra text.\
"""

_api_key = os.getenv("GEMINI_API_KEY")
if not _api_key:
    raise ValueError(
        "GEMINI_API_KEY environment variable is not set. "
        "Add it to your .env file before importing this module."
    )

_client = genai.Client(api_key=_api_key)


def classify_pdf_with_gemini(pdf_path: str) -> dict:
    """
    Classify a fax PDF using Gemini Flash.

    Sends the PDF inline and requests JSON output with
    category, patient_name, and patient_dob fields.

    Returns a dict with keys: gemini_category, gemini_patient_name, gemini_patient_dob.
    On any failure, returns {"gemini_category": "error", "gemini_patient_name": "", "gemini_patient_dob": ""}.
    """
    fax_id = os.path.splitext(os.path.basename(pdf_path))[0]
    try:
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        response = _client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                _PROMPT,
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

        data = json.loads(response.text)

        category = data.get("category", "")
        if category not in VALID_CATEGORIES:
            print(
                f"[gemini_classifier] {fax_id}: unexpected category {category!r}",
                file=sys.stderr,
            )
            return dict(_ERROR_DICT)

        raw_dob = data.get("patient_dob", "") or ""
        if raw_dob:
            try:
                raw_dob = dateparser.parse(raw_dob).strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                raw_dob = ""

        return {
            "gemini_category": category,
            "gemini_patient_name": data.get("patient_name", "") or "",
            "gemini_patient_dob": raw_dob,
        }

    except Exception as exc:
        print(
            f"[gemini_classifier] {fax_id}: {exc}",
            file=sys.stderr,
        )
        return dict(_ERROR_DICT)
