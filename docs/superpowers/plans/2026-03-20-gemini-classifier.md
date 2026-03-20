# Gemini Classifier Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `modules/gemini_classifier.py` that sends fax PDFs to Gemini Flash and returns category + patient info, then wire its output into `classify_received_faxes.py` as three new TSV columns alongside the existing keyword classifier.

**Architecture:** A single new module exposes one public function `classify_pdf_with_gemini(pdf_path)`. It base64-encodes the PDF inline, calls Gemini Flash with `response_mime_type="application/json"`, maps the returned `category`/`patient_name`/`patient_dob` keys to their `gemini_*` equivalents, normalizes the DOB, and returns a safe error dict on any failure. The classifier script imports this function and adds three columns to the TSV.

**Tech Stack:** `google-genai` SDK, `python-dateutil`, `python-dotenv`, `pytest` + `unittest.mock`

---

## File Map

| Action | File | Purpose |
|--------|------|---------|
| Modify | `requirements.txt` | Add `google-genai` |
| Create | `modules/gemini_classifier.py` | New Gemini classifier module |
| Create | `tests/test_gemini_classifier.py` | Unit tests (mocked API) |
| Modify | `classify_received_faxes.py` | Import and call Gemini classifier, update TSV |

---

## Task 1: Add dependency

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Add `google-genai` to requirements**

Open `requirements.txt` and add `google-genai` as a new line (keep the list alphabetically ordered — insert after `alive_progress` and before `boto3`, or at the appropriate alphabetical position).

- [ ] **Step 2: Install it**

```bash
pip install google-genai
```

Expected: installs without error.

- [ ] **Step 3: Commit**

```bash
git add requirements.txt
git commit -m "feat: add google-genai dependency for Gemini classifier"
```

---

## Task 2: Write `modules/gemini_classifier.py` (TDD)

**Files:**
- Create: `tests/test_gemini_classifier.py`
- Create: `modules/gemini_classifier.py`

### Step 1 — Write the failing tests

- [ ] Create `tests/test_gemini_classifier.py`:

```python
"""Unit tests for modules/gemini_classifier.py — all API calls are mocked."""
import json
import os
from unittest.mock import MagicMock, mock_open, patch

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_RESPONSE = {
    "category": "result - routine",
    "patient_name": "Jane Doe",
    "patient_dob": "03/15/1980",
}

ERROR_DICT = {"gemini_category": "error", "gemini_patient_name": "", "gemini_patient_dob": ""}

CATEGORIES = ["result - routine", "result - urgent", "scheduling", "insurance", "other"]


def make_mock_response(payload: dict) -> MagicMock:
    """Return a mock Gemini response whose .text is JSON-serialised payload."""
    mock = MagicMock()
    mock.text = json.dumps(payload)
    return mock


def make_client_mock(payload: dict) -> MagicMock:
    """Return a mock google.genai Client whose generate_content returns payload."""
    client = MagicMock()
    client.models.generate_content.return_value = make_mock_response(payload)
    return client


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestClassifyPdfWithGemini:
    """Tests for classify_pdf_with_gemini."""

    def _call(self, client_mock, pdf_bytes=b"%PDF-fake"):
        """Helper: call the function with a mocked client and fake PDF bytes."""
        from modules.gemini_classifier import classify_pdf_with_gemini

        with patch("modules.gemini_classifier._client", client_mock), \
             patch("builtins.open", mock_open(read_data=pdf_bytes)):
            return classify_pdf_with_gemini("fake/path/1234.pdf")

    def test_returns_correct_keys(self):
        result = self._call(make_client_mock(VALID_RESPONSE))
        assert set(result.keys()) == {"gemini_category", "gemini_patient_name", "gemini_patient_dob"}

    def test_maps_category_key(self):
        result = self._call(make_client_mock(VALID_RESPONSE))
        assert result["gemini_category"] == "result - routine"

    def test_maps_patient_name_key(self):
        result = self._call(make_client_mock(VALID_RESPONSE))
        assert result["gemini_patient_name"] == "Jane Doe"

    def test_normalizes_dob_to_iso(self):
        result = self._call(make_client_mock(VALID_RESPONSE))
        assert result["gemini_patient_dob"] == "1980-03-15"

    def test_empty_dob_stays_empty(self):
        payload = {**VALID_RESPONSE, "patient_dob": ""}
        result = self._call(make_client_mock(payload))
        assert result["gemini_patient_dob"] == ""

    def test_dob_already_iso_format(self):
        payload = {**VALID_RESPONSE, "patient_dob": "1990-06-01"}
        result = self._call(make_client_mock(payload))
        assert result["gemini_patient_dob"] == "1990-06-01"

    @pytest.mark.parametrize("category", CATEGORIES)
    def test_all_valid_categories_accepted(self, category):
        payload = {**VALID_RESPONSE, "category": category}
        result = self._call(make_client_mock(payload))
        assert result["gemini_category"] == category

    def test_invalid_category_returns_error(self):
        payload = {**VALID_RESPONSE, "category": "not-a-category"}
        result = self._call(make_client_mock(payload))
        assert result == ERROR_DICT

    def test_api_exception_returns_error(self):
        client = MagicMock()
        client.models.generate_content.side_effect = RuntimeError("API down")
        result = self._call(client)
        assert result == ERROR_DICT

    def test_malformed_json_returns_error(self):
        client = MagicMock()
        bad_response = MagicMock()
        bad_response.text = "this is not json"
        client.models.generate_content.return_value = bad_response
        result = self._call(client)
        assert result == ERROR_DICT

    def test_missing_category_key_returns_error(self):
        payload = {"patient_name": "Jane Doe", "patient_dob": ""}
        result = self._call(make_client_mock(payload))
        assert result == ERROR_DICT

    def test_missing_dob_key_returns_empty(self):
        payload = {"category": "other", "patient_name": ""}
        result = self._call(make_client_mock(payload))
        assert result["gemini_patient_dob"] == ""
        assert result["gemini_category"] == "other"

    def test_empty_patient_name_allowed(self):
        payload = {**VALID_RESPONSE, "patient_name": ""}
        result = self._call(make_client_mock(payload))
        assert result["gemini_patient_name"] == ""
        assert result["gemini_category"] != "error"


class TestModuleInit:
    """Test that the module raises early when GEMINI_API_KEY is missing."""

    def test_raises_on_missing_api_key(self, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        import sys
        # Remove cached module so re-import runs module-level code.
        # Mock genai.Client to avoid the real SDK validating credentials.
        sys.modules.pop("modules.gemini_classifier", None)
        with patch("google.genai.Client"), \
             pytest.raises(ValueError, match="GEMINI_API_KEY"):
            import modules.gemini_classifier  # noqa: F401
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_gemini_classifier.py -v
```

Expected: `ModuleNotFoundError` or `ImportError` — `modules/gemini_classifier.py` does not exist yet.

### Step 3 — Implement the module

- [ ] Create `modules/gemini_classifier.py`:

```python
"""
Gemini-powered fax classifier.

Sends the raw PDF bytes to Gemini Flash and returns a classification
and patient info as a dict. Used as a second opinion alongside the
keyword-based classifier in modules/fax_classifier.py.
"""

import base64
import json
import os
import sys

from dateutil import parser as dateparser
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

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

    Sends the PDF inline (base64-encoded) and requests JSON output with
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_gemini_classifier.py -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add modules/gemini_classifier.py tests/test_gemini_classifier.py
git commit -m "feat: add Gemini classifier module with tests"
```

---

## Task 3: Wire Gemini classifier into `classify_received_faxes.py`

**Files:**
- Modify: `classify_received_faxes.py`

The updated TSV column order is:
```
fax_id | document_type | confidence | manual_category | gemini_category | from_number | created_at | patient_name | gemini_patient_name | patient_dob | gemini_patient_dob | healthie_id
```

Note: `confidence` moves before `manual_category` compared to the current header.

- [ ] **Step 1: Add the import**

In `classify_received_faxes.py`, add after the existing module imports:

```python
from modules.gemini_classifier import classify_pdf_with_gemini
```

- [ ] **Step 2: Call the classifier and update `rows.append`**

In `run_classify`, after the `healthie_id` lookup (currently line ~129), add the Gemini call and expand the row dict:

Replace:
```python
            rows.append({
                "fax_id": fax_id,
                "document_type": result["document_type"],
                "manual_category": manual.get(fax_id, ""),
                "confidence": result["confidence"],
                "from_number": meta.get("from_number", ""),
                "created_at": meta.get("created_at", ""),
                "patient_name": result["patient_name"],
                "patient_dob": result["patient_dob"],
                "healthie_id": healthie_id or "n/a",
            })
```

With:
```python
            gemini = classify_pdf_with_gemini(pdf_path)
            rows.append({
                "fax_id": fax_id,
                "document_type": result["document_type"],
                "confidence": result["confidence"],
                "manual_category": manual.get(fax_id, ""),
                "gemini_category": gemini["gemini_category"],
                "from_number": meta.get("from_number", ""),
                "created_at": meta.get("created_at", ""),
                "patient_name": result["patient_name"],
                "gemini_patient_name": gemini["gemini_patient_name"],
                "patient_dob": result["patient_dob"],
                "gemini_patient_dob": gemini["gemini_patient_dob"],
                "healthie_id": healthie_id or "n/a",
            })
```

- [ ] **Step 3: Update the TSV header and row writer**

Replace:
```python
    with open(output_tsv, "w") as f:
        f.write("fax_id\tdocument_type\tmanual_category\tconfidence\tfrom_number\tcreated_at\tpatient_name\tpatient_dob\thealthie_id\n")
        for row in rows:
            f.write(
                f"{row['fax_id']}\t{row['document_type']}\t{row['manual_category']}\t"
                f"{row['confidence']}\t{row['from_number']}\t{row['created_at']}\t"
                f"{row['patient_name']}\t{row['patient_dob']}\t{row['healthie_id']}\n"
            )
```

With:
```python
    with open(output_tsv, "w") as f:
        f.write(
            "fax_id\tdocument_type\tconfidence\tmanual_category\tgemini_category\t"
            "from_number\tcreated_at\t"
            "patient_name\tgemini_patient_name\tpatient_dob\tgemini_patient_dob\thealthie_id\n"
        )
        for row in rows:
            f.write(
                f"{row['fax_id']}\t{row['document_type']}\t{row['confidence']}\t"
                f"{row['manual_category']}\t{row['gemini_category']}\t"
                f"{row['from_number']}\t{row['created_at']}\t"
                f"{row['patient_name']}\t{row['gemini_patient_name']}\t"
                f"{row['patient_dob']}\t{row['gemini_patient_dob']}\t{row['healthie_id']}\n"
            )
```

- [ ] **Step 4: Run full test suite**

```bash
pytest tests/ -v
```

Expected: all existing tests plus the new Gemini tests pass.

- [ ] **Step 5: Smoke test on a single fax**

Make sure `GEMINI_API_KEY` is in your `.env`, then run against one PDF to check the output:

```bash
python - <<'EOF'
from modules.gemini_classifier import classify_pdf_with_gemini
import json
result = classify_pdf_with_gemini("received_faxes/1395164.pdf")
print(json.dumps(result, indent=2))
EOF
```

Expected: a dict with `gemini_category` set to one of the five valid values, and plausible `gemini_patient_name` / `gemini_patient_dob`.

- [ ] **Step 6: Commit**

```bash
git add classify_received_faxes.py
git commit -m "feat: wire Gemini classifier into classify_received_faxes TSV output"
```
