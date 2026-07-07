# Email Assistant

AI-powered writing assistant with a PyQt6 desktop frontend and FastAPI backend. Integrates with Ollama for local LLM inference to provide grammar correction, text rewriting, and professional tone transformation.

## Quick Start

```bash
# Install dependencies
uv sync

# Start backend (FastAPI)
uv run uvicorn backend.app:app --reload

# Run frontend (PyQt6)
uv run python frontend/main.py
```

## Architecture

```
backend/                    # FastAPI backend service
├── app.py                  # FastAPI app with /generate endpoint
├── config.py               # Ollama config (OLLAMA_URL, OLLAMA_MODEL)
├── models/                 # Pydantic request/response models
├── prompts/                # Prompt templates (registry pattern)
│   ├── registry.py         # PROMPTS dict — add new actions here
│   └── <action>.py         # build_prompt(text) -> str
└── services/
    ├── generator.py        # Orchestrates prompt + LLM call
    └── llm.py              # Ollama HTTP client

frontend/                   # PyQt6 desktop app
├── main.py                 # Entry point
├── config.py               # Backend API endpoint
├── services/
│   └── api_client.py       # httpx.post() wrapper for /generate
└── ui/
    └── main_window.py      # MainWindow with buttons + output
```

## API Contract

```
POST http://127.0.0.1:8000/generate
Content-Type: application/json

Request: {"action": "grammar", "text": "user input"}
Response: {"action": "grammar", "text": "user input", "suggestion": ["corrected text"]}
```

## Environment Setup

- Copy `backend/.env.example` to `backend/.env`
- Required env vars:
  - `OLLAMA_URL=http://localhost:11434/api/generate`
  - `OLLAMA_MODEL=gemma3:4b`
- Ollama must be running locally; model must be pulled: `ollama pull gemma3:4b`

## Adding a New AI Action

1. Create `backend/prompts/<name>.py` with a `build_prompt(text: str) -> str` function
2. Register in `backend/prompts/registry.py` under `PROMPTS["<action>"]`
3. Add button to `frontend/ui/main_window.py`
4. Wire up click handler calling `self.api_client.generate(action="<action>", ...)`

## Known Issues

- Incomplete button handlers (grammar/professional only print, don't call API)
- No error handling in frontend or LLM client
- No threading — UI freezes during LLM generation
- No user input field — hardcoded text in handlers

## Related

- See `AGENTS.md` for AI coding agent instructions
- See `CLAUDE.md` for Claude Code-specific guidance
