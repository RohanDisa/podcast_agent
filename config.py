
from __future__ import annotations

import os
from typing import Optional

from helper import load_env

# Load environment variables from .env if available
load_env()

# Google Gemini API Key
# Attempt to import from config_secret.py (ignored from version control)
try:  # pragma: no cover - import guard
    from config_secret import GEMINI_API_KEY as _SECRET_KEY  # type: ignore
except ModuleNotFoundError:
    _SECRET_KEY: Optional[str] = None
else:
    _SECRET_KEY = _SECRET_KEY.strip()

# Fallback to environment variable or placeholder
GEMINI_API_KEY = (
    _SECRET_KEY
    or os.getenv("GEMINI_API_KEY")
    or "your-gemini-api-key-here"
)

# Model configurations
# Google search tool requires Gemini models that support function calling
# Using gemini-2.5-flash-lite-preview-09-2025 as requested
PODCASTER_MODEL = "gemini-2.5-flash-lite-preview-09-2025"
ROOT_AGENT_MODEL = "gemini-2.5-flash-lite-preview-09-2025"
TTS_MODEL = "gemini-2.5-flash-preview-tts"  # TTS model from original notebook

# Whitelisted news domains
WHITELIST_DOMAINS = [
    "techcrunch.com",
    "venturebeat.com",
    "theverge.com",
    "technologyreview.com",
    "arstechnica.com"
]

# File names
REPORT_FILENAME = "ai_research_report.md"
PODCAST_FILENAME = "ai_today_podcast.wav"

# TTS Configuration
SPEAKER_CONFIGS = {
    "Joe": {
        "voice_name": "Kore"
    },
    "Jane": {
        "voice_name": "Puck"
    }
}

