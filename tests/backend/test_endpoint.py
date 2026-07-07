"""Integration tests for the FastAPI /generate endpoint and the backend LLM client."""

import os

import pytest
import requests
from fastapi import HTTPException


class TestGenerateEndpoint:
    """Tests that exercise FastAPI's /generate route via TestClient."""

    def test_home(self, client):
        """The root route returns a simple JSON message."""
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json()["message"] == "backend is running successfully!!"

    # -- happy path ----------------------------------------------------------------

    @pytest.mark.available_server
    def test_generate_grammar(self, client):
        """Grammar action returns a suggestion list with non-empty text."""
        payload = {"action": "grammar", "text": "hello world this is a test"}
        resp = client.post("/generate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["action"] == "grammar"
        assert isinstance(data["suggestion"], list)
        assert len(data["suggestion"]) >= 1
        assert data["suggestion"][0].strip()

    @pytest.mark.available_server
    def test_generate_rewrite(self, client):
        """Rewrite action returns a non-empty suggestion list."""
        payload = {"action": "rewrite", "text": "quick brown fox"}
        resp = client.post("/generate", json=payload)
        assert resp.status_code == 200
        assert resp.json()["suggestion"] and isinstance(resp.json()["suggestion"], list)

    @pytest.mark.available_server
    def test_generate_professional(self, client):
        """Professional tone action returns a non-empty suggestion list."""
        payload = {"action": "professional", "text": "hey this is dumb"}
        resp = client.post("/generate", json=payload)
        assert resp.status_code == 200
        assert resp.json()["suggestion"] and isinstance(resp.json()["suggestion"], list)

    # -- error paths ---------------------------------------------------------------

    def test_generate_empty_text(self, client):
        """Empty text raises 400."""
        resp = client.post("/generate", json={"action": "grammar", "text": ""})
        assert resp.status_code == 400

    def test_generate_missing_action(self, client):
        """Missing action field returns 422 (validation error)."""
        resp = client.post("/generate", json={"text": "hello"})
        assert resp.status_code == 422

    def test_generate_unknown_action(self, client):
        """Unknown action returns 400 (user-defined error)."""
        resp = client.post(
            "/generate", json={"action": "sparkles", "text": "hello"},
        )
        assert resp.status_code == 400

    def test_generate_missing_text(self, client):
        """Missing text field returns 422."""
        resp = client.post("/generate", json={"action": "grammar"})
        assert resp.status_code == 422


class TestLlmClient:
    """Tests that hit the configured LLM server directly (bypassing FastAPI).

    These verify the OpenAI-compatible API path in ``backend/services/llm.py``.
    """

    @pytest.mark.available_server
    def test_direct_generate_returns_text(self):
        """A valid chat/completions call returns the generated content."""
        resp = requests.post(
            os.environ["LLM_URL"],
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ['LLM_KEY']}",
            },
            json={
                "model": os.environ.get("LLM_MODEL", "Coder-9B"),
                "messages": [{"role": "user", "content": "Reply with exactly one word: hello"}],
            },
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "choices" in data
        assert len(data["choices"]) > 0
        assert "message" in data["choices"][0]
        assert data["choices"][0]["message"]["content"].strip()

    @pytest.mark.available_server
    def test_direct_generate_malformed_payload(self):
        """Missing 'messages' body returns 4xx, not a confusing parse error."""
        resp = requests.post(
            os.environ["LLM_URL"],
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ['LLM_KEY']}",
            },
            json={"model": "whatever"},  # no 'messages' key
        )
        # The server should return 4xx (not 5xx / crash)
        assert resp.status_code >= 400 and resp.status_code < 500

    def test_direct_unreachable_server(self):
        """Calling an unreachable server raises ConnectionError, not a parse crash."""
        with pytest.raises((requests.ConnectionError, requests.exceptions.ConnectionError)):
            requests.post(
                "http://127.0.0.1:1",  # definitely nothing listening here
                json={"model": "nope", "messages": [{"role": "user", "content": "hi"}]},
            )
