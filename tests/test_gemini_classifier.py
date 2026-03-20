"""Unit tests for modules/gemini_classifier.py — all API calls are mocked."""

import json
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

ERROR_DICT = {
    "gemini_category": "error",
    "gemini_patient_name": "",
    "gemini_patient_dob": "",
}

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

        with (
            patch("modules.gemini_classifier._client", client_mock),
            patch("builtins.open", mock_open(read_data=pdf_bytes)),
        ):
            return classify_pdf_with_gemini("fake/path/1234.pdf")

    def test_returns_correct_keys(self):
        result = self._call(make_client_mock(VALID_RESPONSE))
        assert set(result.keys()) == {
            "gemini_category",
            "gemini_patient_name",
            "gemini_patient_dob",
        }

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
        with (
            patch("google.genai.Client"),
            pytest.raises(ValueError, match="GEMINI_API_KEY"),
        ):
            import modules.gemini_classifier  # noqa: F401
