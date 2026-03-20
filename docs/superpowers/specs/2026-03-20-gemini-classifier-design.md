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

Exactly five allowed values:

- `result - routine`
- `result - urgent`
- `scheduling`
- `insurance`
- `other`

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

### Implementation

1. Read PDF bytes from `pdf_path` and base64-encode them.
2. Send to Gemini Flash via the `google-generativeai` SDK using inline `inline_data` with MIME type `application/pdf`.
3. Prompt instructs Gemini to return a JSON object with exactly three fields: `category`, `patient_name`, `patient_dob`.
4. Parse the JSON response. Normalize `patient_dob` to `YYYY-MM-DD` using `python-dateutil`.
5. Validate that `category` is one of the 5 allowed values; if not, treat as `"error"`.

### API key

Read from `GEMINI_API_KEY` environment variable via `python-dotenv` (already in use in this project).

### Error handling

Any exception — API failure, malformed JSON, unexpected category value, missing env var — returns:
```python
{"gemini_category": "error", "gemini_patient_name": "", "gemini_patient_dob": ""}
```
This ensures a single bad fax never aborts a full run.

### Constraints

- PDF file size limit: 20MB per inline request (largest fax in corpus is 464KB — well within limit).
- Model: `gemini-2.0-flash` (or latest stable Flash equivalent).
- No caching: at ~762 faxes and negligible cost (~$0.03 total), caching adds complexity without benefit.

---

## Changes to `classify_received_faxes.py`

- Add import of `classify_pdf_with_gemini` from `modules.gemini_classifier`.
- In `run_classify`, call `classify_pdf_with_gemini(pdf_path)` for each fax.
- Add three new columns to the TSV output, placed immediately after `manual_category`:
  - `gemini_category`
  - `gemini_patient_name`
  - `gemini_patient_dob`
- No changes to `run_discover`.

### Updated TSV column order

```
fax_id | document_type | manual_category | gemini_category | gemini_patient_name | gemini_patient_dob | confidence | from_number | created_at | patient_name | patient_dob | healthie_id
```

---

## Dependencies

Add to `requirements.txt`:
- `google-generativeai`

---

## Out of Scope

- Replacing the existing keyword classifier (kept for comparison).
- Caching Gemini results between runs.
- Using Gemini for the Healthie user ID lookup.
- Subcategory breakdown beyond the 5 defined categories.
