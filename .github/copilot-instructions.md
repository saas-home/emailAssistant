# GitHub Copilot Instructions for Email Assistant

## Project Overview

AI-powered writing assistant with PyQt6 desktop frontend and FastAPI backend. Integrates with Ollama for local LLM inference.

## Quick Start

```bash
uv sync
uv run uvicorn backend.app:app --reload   # backend
uv run python frontend/main.py            # frontend
```

## Architecture

- **Backend**: FastAPI with `/generate` endpoint, Ollama LLM client, prompt registry
- **Frontend**: PyQt6 desktop app with buttons + QPlainTextEdit output
- **Communication**: HTTP REST API (httpx → FastAPI → requests → Ollama)

## Key Conventions

- Files: `snake_case`, Functions: `snake_case`, Classes: `PascalCase`, Constants: `UPPER_SNAKE_CASE`
- Prompt registry: `backend/prompts/registry.py` — add new actions by creating `build_prompt(text)` function and registering in `PROMPTS` dict
- `suggestion` field is always a **list of one string** — LLM response wrapped in list by `generator.py`
- Frontend timeout: 120 seconds

## Adding a New AI Action

1. Create `backend/prompts/<name>.py` with `build_prompt(text: str) -> str`
2. Register in `backend/prompts/registry.py` under `PROMPTS["<action>"]`
3. Add button to `frontend/ui/main_window.py`
4. Wire up click handler

## Known Issues

- Incomplete button handlers (grammar/professional only print, don't call API)
- No error handling in frontend or LLM client
- No threading — UI freezes during LLM generation
- No user input field — hardcoded text in handlers

## Related

- See `AGENTS.md` for full agent instructions
- See `CLAUDE.md` for Claude Code-specific guidance
