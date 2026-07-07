# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Email Assistant** is an AI-powered writing assistant application with a PyQt6 desktop frontend and FastAPI backend. It integrates with Ollama for local LLM inference to provide grammar correction, text rewriting, and professional tone transformation.

## Architecture

```
emailAssistant/
├── backend/                    # FastAPI backend service
│   ├── app.py                  # FastAPI application with /generate endpoint
│   ├── config.py               # Ollama API configuration (OLLAMA_URL, OLLAMA_MODEL)
│   ├── models/                 # Pydantic request/response models
│   ├── prompts/                # Prompt templates for different AI actions
│   │   ├── grammar.py          # Grammar correction prompt
│   │   ├── professional.py     # Professional tone prompt
│   │   ├── rewrite.py          # Rewriting prompt
│   │   ├── registry.py         # Central prompt registry (PROMPTS dict)
│   │   └── __init__.py
│   ├── services/               # Core business logic
│   │   ├── generator.py        # Orchestrates prompt selection + LLM calls
│   │   └── llm.py              # Ollama API client (HTTP requests)
│   └── ui/                     # PyQt6 desktop UI
├── frontend/                   # PyQt6 desktop application
│   ├── main.py                 # Application entry point
│   ├── app.py                  # Main window with buttons + QPlainTextEdit output
│   ├── config.py               # Backend API endpoint (http://127.0.0.1:8000/generate)
│   ├── services/               # HTTP client for backend communication
│   │   └── api_client.py       # httpx.post() wrapper for /generate endpoint
│   └── ui/                     # Main window implementation
└── pyproject.toml              # Project dependencies (uv/pip compatible)
```

## Key Design Patterns

1. **Prompt Registry Pattern**: `backend/prompts/registry.py` centralizes all prompt builders in a `PROMPTS` dictionary keyed by action name. This enables easy addition of new AI capabilities without modifying the core generator logic.

2. **Service Layer Separation**: `generator.py` handles orchestration (prompt selection, validation), while `llm.py` is a thin HTTP client. This allows swapping LLM providers by replacing the service implementation.

3. **Frontend-Backend Decoupling**: The PyQt6 frontend communicates exclusively via HTTP to the FastAPI backend. The `ApiClient` class encapsulates all remote calls with a 120-second timeout.

## Development Commands

### Backend (FastAPI)
```bash
# Start backend server
uv run uvicorn backend.app:app --reload

# Test endpoint locally (curl)
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"action": "grammar", "text": "helow world"}'
```

### Frontend (PyQt6)
```bash
# Run desktop application
uv run python frontend/main.py

# Debug with source map
uv run python -m pdb frontend/main.py
```

### Environment Configuration
The backend reads Ollama settings from `frontend/.env` (copied from `.env.example`):
- `OLLAMA_URL=http://localhost:11434/api/generate`
- `OLLAMA_MODEL=gemma3:4b`

## Common Workflows

### Adding a New AI Action
1. Add prompt builder to `backend/prompts/<name>.py` with function signature `build_prompt(text: str) -> str`
2. Register in `backend/prompts/registry.py` under `PROMPTS["<action>"]`
3. Add corresponding button to `frontend/ui/main_window.py`
4. Wire up click handler calling `self.api_client.generate(action="<action>", ...)`

### Debugging LLM Issues
- Verify Ollama is running: `curl http://localhost:11434/api/tags`
- Test raw Ollama endpoint directly with the payload from `backend/services/llm.py`
- Check backend logs for HTTP 500 errors when LLM fails

## Data Flow
1. User clicks button → `MainWindow.clicked()` handler
2. Frontend calls `ApiClient.generate(action, text)` via HTTP POST
3. Backend `/generate` endpoint validates Pydantic models
4. `generator.py` selects prompt template from registry, builds full prompt
5. `llm.py` sends JSON payload to Ollama API
6. Response flows back through the stack to display in QPlainTextEdit

## API Contract

```
POST http://127.0.0.1:8000/generate
Content-Type: application/json

Request:  {"action": "grammar", "text": "user input"}
Response: {"action": "grammar", "text": "user input", "suggestion": ["corrected text"]}
```

- `suggestion` is always a **list of one string** — the LLM response is wrapped in a list by `generator.py`
- Frontend uses `httpx.post()` with a **120-second timeout**
- Backend uses `requests.post()` (sync) to call Ollama

## Known Issues & Gotchas

1. **Incomplete button handlers**: `grammar_clicked()` and `professional_clicked()` only print to console — they don't call the API or update the output box. Only `rewrite_clicked()` is fully implemented.
2. **Hardcoded text**: `rewrite_clicked()` uses a hardcoded sample text instead of reading from an input field. There is no text input widget in the UI.
3. **No error handling** in frontend `ApiClient.generate()` or backend LLM client — `response.json()` without status check will crash if the service is down.
4. **No threading** in PyQt6 — the 120-second API timeout freezes the UI during LLM generation.
5. **`suggestion` is always a list of one string** — fragile if the LLM returns an empty response.
6. **No input validation** on the frontend — no user input field exists.

## Tests

No test framework or test files are present in this project. If adding tests later:
- Use `pytest` (add to `pyproject.toml` dependencies)
- The `generator.generate_suggestion()` function is pure logic and ideal for unit tests (mock `llm.generate` to avoid Ollama dependency)
