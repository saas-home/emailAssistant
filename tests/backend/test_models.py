"""Unit tests for Pydantic request/response models."""

import pytest
from pydantic import ValidationError

from backend.models.request_models import GenerateRequest
from backend.models.response_models import GenerateResponse

class TestGenerateRequest:
    """Tests for the GenerateRequest Pydantic model."""

    def test_valid_request(self):
        """Valid request creates successfully."""
        req = GenerateRequest(action="grammar", text="hello world")
        assert req.action == "grammar"
        assert req.text == "hello world"

    def test_missing_action_raises_validation(self):
        """Missing action field raises ValidationError."""
        with pytest.raises(ValidationError):
            GenerateRequest(text="hello")

    def test_missing_text_raises_validation(self):
        """Missing text field raises ValidationError."""
        with pytest.raises(ValidationError):
            GenerateRequest(action="grammar")

    def test_empty_action_is_valid(self):
        """Empty action string is technically valid (validation happens in service)."""
        req = GenerateRequest(action="", text="hello")
        assert req.action == ""
        assert req.text == "hello"

    def test_empty_text_is_valid(self):
        """Empty text string is technically valid (validation happens in service)."""
        req = GenerateRequest(action="grammar", text="")
        assert req.action == "grammar"
        assert req.text == ""

    def test_whitespace_text_is_valid(self):
        """Whitespace-only text is technically valid (validation happens in service)."""
        req = GenerateRequest(action="grammar", text="   ")
        assert req.text == "   "

    def test_long_text_is_valid(self):
        """Very long text is accepted by the model."""
        long_text = "word " * 10000
        req = GenerateRequest(action="grammar", text=long_text)
        assert len(req.text) == 50000

    def test_unicode_text_is_valid(self):
        """Unicode text is accepted by the model."""
        req = GenerateRequest(action="grammar", text="こんにちは世界")
        assert req.text == "こんにちは世界"

class TestGenerateResponse:
    """Tests for the GenerateResponse Pydantic model."""

    def test_valid_response(self):
        """Valid response creates successfully."""
        resp = GenerateResponse(
            action="grammar",
            text="hello",
            suggestion=["corrected text"]
        )
        assert resp.action == "grammar"
        assert resp.text == "hello"
        assert resp.suggestion == ["corrected text"]

    def test_suggestion_must_be_list(self):
        """Suggestion must be a list, not a string."""
        with pytest.raises(ValidationError):
            GenerateResponse(action="grammar", text="hello", suggestion="not a list")

    def test_suggestion_must_contain_strings(self):
        """Suggestion list must contain strings."""
        with pytest.raises(ValidationError):
            GenerateResponse(action="grammar", text="hello", suggestion=[123])

    def test_suggestion_can_be_empty_list(self):
        """Empty suggestion list is technically valid."""
        resp = GenerateResponse(action="grammar", text="hello", suggestion=[])
        assert resp.suggestion == []

    def test_suggestion_can_have_multiple_items(self):
        """Suggestion list can have multiple items."""
        resp = GenerateResponse(
            action="grammar",
            text="hello",
            suggestion=["suggestion 1", "suggestion 2"]
        )
        assert len(resp.suggestion) == 2
