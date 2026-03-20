# Gemini Classifier — Design Spec

**Date:** 2026-03-20
**Status:** Approved

---

## Background

The existing fax classifier (`modules/fax_classifier.py`) uses keyword regex rules to classify received faxes and extract patient name/DOB. OCR quality issues (e.g. misread dates) reduce extraction accuracy. Gemini's native PDF understanding provides a more robust second opinion without relying on OCR text.

---

## Goal

Add a Gemini-powered classifier that reads PDFs directly and returns:
- A document category
- Patient name
- Patient DOB

Results appear as additional columns in `received_fax_types.tsv` for side-by-side comparison with the existing keyword classifier and the manually assigned ground truth.

---

## Categories

Exactly five allowed values (lowercase, intentionally different from the title-case values used by the existing keyword classifier in `document_type`):

- `result - routine`
- `result - urgent`
- `scheduling`
- `insurance`
- `other`

The `gemini_category` column uses this lowercase convention. No normalization is applied to align it with `document_type` — the difference is intentional to keep the two classifiers independently readable.

---

## New Module: `modules/gemini_classifier.py`

### Public interface

```python
def classify_pdf_with_gemini(pdf_path: str) -> dict:
    ...
```

**Returns:**
```python
{
    "gemini_category":     str,  # one of the 5 categories, or "error"
    "gemini_patient_name": str,  # empty string if not found
    "gemini_patient_dob":  str,  # YYYY-MM-DD if found, else empty string
}
```

### SDK and package

Use the **`google-genai`** package (import: `google.genai`), which is the current stable Gemini Python SDK as of 2025. Add `google-genai` to `requirements.txt`.

Do **not** use the legacy `google-generativeai` package.

### Implementation

1. Read PDF bytes from `pdf_path` and pass them inline using `types.Part.from_bytes(data=bytes, mime_type="application/pdf")`.
2. Build the request with `client.models.generate_content(...)`, passing the inline PDF part alongside the prompt.
3. Set `response_mime_type="application/json"` in `GenerationConfig` to force a clean JSON response (no markdown fencing). This makes `json.loads(response.text)` reliable.
4. The JSON returned by the model uses the key `category` (as defined in the prompt); map this to `gemini_category` in the returned dict. Similarly map `patient_name` → `gemini_patient_name` and `patient_dob` → `gemini_patient_dob`.
5. Normalize `gemini_patient_dob` to `YYYY-MM-DD` using `python-dateutil` if a value is present; leave as empty string if absent.
6. Validate that `gemini_category` is one of the 5 allowed values; if not, treat as `"error"`.

### Prompt

```
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

Return only the JSON object. No explanation, no markdown, no extra text.
```

### API key

Read from `GEMINI_API_KEY` environment variable via `python-dotenv` (already in use in this project).

### Error handling

Any exception — API failure, malformed JSON, unexpected category value, missing env var, unreadable file — logs the exception message to stderr with the fax ID for context, then returns:
```python
{"gemini_category": "error", "gemini_patient_name": "", "gemini_patient_dob": ""}
```
This ensures a single bad fax never aborts a full run, and failures are visible in the terminal output.

### Constraints

- PDF file size limit: 20MB per inline request (largest fax in corpus is 464KB — well within limit).
- Model: defined as a module-level constant `GEMINI_MODEL = "gemini-2.0-flash"` so it can be updated in one place. If `GEMINI_API_KEY` is missing, raise `ValueError` at module import time (fail fast) rather than discovering it on the first fax.
- No caching: at ~762 faxes and negligible cost (~$0.03 total), caching adds complexity without benefit.

---

## Changes to `classify_received_faxes.py`

- Add import of `classify_pdf_with_gemini` from `modules.gemini_classifier`.
- In `run_classify`, call `classify_pdf_with_gemini(pdf_path)` for each fax.
- Add three new columns to the TSV output: `gemini_category` (after `manual_category`), `gemini_patient_name` (after `patient_name`), and `gemini_patient_dob` (after `patient_dob`).
- Update the header string, the `rows.append({...})` dict, and the row `f.write(...)` format string in `run_classify` to include these three fields in the correct positions.
- No changes to `run_discover`.

### Updated TSV column order

```
fax_id | document_type | confidence | manual_category | gemini_category | from_number | created_at | patient_name | gemini_patient_name | patient_dob | gemini_patient_dob | healthie_id
```

---

## Dependencies

Add to `requirements.txt`:
- `google-genai`

---

## Out of Scope

- Replacing the existing keyword classifier (kept for comparison).
- Caching Gemini results between runs.
- Using Gemini for the Healthie user ID lookup.
- Subcategory breakdown beyond the 5 defined categories.
