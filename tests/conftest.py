"""Pytest configuration for the test suite."""

from dotenv import load_dotenv

# Load .env once at session start so GEMINI_API_KEY and other vars are
# available in os.environ before any test imports application modules.
load_dotenv()
