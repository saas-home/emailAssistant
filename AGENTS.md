# AGENTS.md

AI coding agent instructions for the **Email Assistant** project.

## Project Overview

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

## Key Conventions

### Naming
- Files: `snake_case` (e.g., `api_client.py`)
- Functions: `snake_case` (e.g., `generate_suggestion`)
- Classes: `PascalCase` (e.g., `ApiClient`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `PROMPTS`)

### Adding a New AI Action
1. Create `backend/prompts/<name>.py` with a `build_prompt(text: str) -> str` function
2. Register in `backend/prompts/registry.py` under `PROMPTS["<action>"]`
3. Add button to `frontend/ui/main_window.py`
4. Wire up click handler calling `self.api_client.generate(action="<action>", ...)`

### API Contract
```
POST http://127.0.0.1:8000/generate
Content-Type: application/json

Request: {"action": "grammar", "text": "user input"}
Response: {"action": "grammar", "text": "user input", "suggestion": ["corrected text"]}
```

- `suggestion` is always a **list of one string** — the LLM response is wrapped in a list by `generator.py`
- Frontend uses `httpx.post()` with a **120-second timeout**
- Backend uses `requests.post()` (sync) to call Ollama

### Error Handling
- Backend: `ValueError` → `HTTPException(status_code=400)`
- Frontend: No error handling currently — `response.json()` without status check
- LLM client: No error handling — `response.json()` without status check

### PyQt6 Patterns
- `MainWindow` extends `QWidget` with `QVBoxLayout`
- Signal-slot: `button.clicked.connect(handler)`
- Output: `QPlainTextEdit` with `setReadOnly(True)`
- Button state: `set_button_enabled(enabled)` during generation
- **No threading** — UI freezes during LLM generation (120s timeout)

## Environment Setup

- Copy `backend/.env.example` to `backend/.env`
- Required env vars:
  - `OLLAMA_URL=http://localhost:11434/api/generate`
  - `OLLAMA_MODEL=gemma3:4b`
- Ollama must be running locally; model must be pulled: `ollama pull gemma3:4b`

## Known Issues & Gotchas

1. **Incomplete button handlers**: `grammar_clicked()` and `professional_clicked()` only print to console — they don't call the API or update the output box. Only `rewrite_clicked()` is fully implemented.
2. **Hardcoded text**: `rewrite_clicked()` uses a hardcoded sample text instead of reading from an input field. There is no text input widget in the UI.
3. **No error handling** in frontend `ApiClient.generate()` or backend LLM client — `response.json()` without status check will crash if the service is down.
4. **No threading** in PyQt6 — the 120-second API timeout freezes the UI during LLM generation.
5. **`suggestion` is always a list of one string** — fragile if the LLM returns an empty response.
6. **No input validation** on the frontend — no user input field exists.

## Related Documentation

- See `CLAUDE.md` for Claude Code-specific guidance (same content, different format)
