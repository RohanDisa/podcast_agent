## AI News Podcast Generator

Generate structured AI news briefings and multi-speaker podcast audio in one click.  
This project is a production-friendly Streamlit app, backed by Google's Agent Development Kit (ADK) and Gemini models.

---

### Highlights
- **Dual-agent orchestration**: a root researcher agent coordinates a dedicated podcaster agent.
- **Trusted sourcing**: searches are automatically restricted to a whitelisted set of tech news domains.
- **End-to-end workflow**: research → financial context → markdown report → conversational script → multi-speaker TTS.
- **Configurable frontend**: Streamlit UI tailored for single-request, chat-style interactions.
- **Pluggable secrets**: Gemini API key is read from `config_secret.py`, `.env`, or environment variables.

---

### Project Layout

```text
.
├── agent.py         # Multi-agent orchestration, tool + callback definitions
├── app.py           # Streamlit frontend (Runner integration, UI)
├── config.py        # Non-secret configuration (models, whitelist, filenames)
├── helper.py        # Environment loader for local development
├── config_secret.py # Local-only secrets (ignored by git)
└── requirements.txt # Python dependencies
```

---

### Prerequisites
- Python 3.13 (virtual environment recommended)
- Google Gemini API access with function-calling support
- Optional: git for version control and deployment workflows

---

### 1. Configure Secrets (Do This First)

- **`config_secret.py` :** Paste your key in this file. 
- **Shell variable (deployments):** if you’re running on a hosted platform, set `GEMINI_API_KEY` as an environment variable there.

`config.py` imports `config_secret.py` when present; otherwise it looks for the environment variable.

---

### 2. Setup

```pwsh
# Create and activate the virtual environment (PowerShell example)
python -m venv podcast
.\podcast\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3. Run the App

```pwsh
streamlit run app.py
```

Open the URL shown in the terminal (usually http://localhost:8501).  
The UI flow:
1. Enter a request (default is provided).
2. Click **“Generate Report & Podcast”**.
3. Wait 1–2 minutes. Progress updates appear in-line.
4. Review/download the markdown report and generated `.wav` podcast.

The sidebar displays the whitelisted news domains the agent trusts while searching.

---

### How It Works

1. **Root Agent (`ai_news_researcher`)**
   - Uses Gemini via ADK Runner (`google.adk.runners.Runner`).
   - Tools: Google Search (whitelist-enforced), financial context fetcher, markdown writer, and the `podcaster_agent`.
   - Strict callback pipeline: filters search domains, enforces recency, and injects sourcing notes into the final report.

2. **Podcaster Agent**
   - Receives the scripted dialogue and invokes `generate_podcast_audio`.
   - Uses Gemini’s multi-speaker TTS (`gemini-2.5-flash-preview-tts` by default).

3. **Streamlit Frontend**
   - Single request UI; results render in-place.
   - No raw agent transcripts shown—only final artifacts.
   - Automatically manages per-run sessions through ADK’s `InMemorySessionService`.

---

### Configuration Reference

Edit `config.py` to tweak non-secret settings:

| Setting | Purpose |
| ------- | ------- |
| `PODCASTER_MODEL`, `ROOT_AGENT_MODEL` | Gemini models for each agent. Defaults to `gemini-2.5-flash-lite-preview-09-2025`. |
| `TTS_MODEL` | Model used for audio generation. |
| `WHITELIST_DOMAINS` | Domains permitted during Google searches. |
| `REPORT_FILENAME`, `PODCAST_FILENAME` | Output filenames for markdown and audio. |
| `SPEAKER_CONFIGS` | Voice names for the TTS speakers. |

---
Happy podcasting! 

