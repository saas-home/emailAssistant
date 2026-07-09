"""Unit tests for the generator service (mocked LLM)."""

import pytest
from unittest.mock import patch

from backend.services.generator import generate_suggestion

class TestGenerateSuggestion:
    """Tests for generator.generate_suggestion — mocked, no LLM server needed."""

    def test_empty_text_raises_value_error(self):
        """Empty text raises ValueError."""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            generate_suggestion("grammar", "")

    def test_whitespace_only_text_raises_value_error(self):
        """Whitespace-only text raises ValueError."""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            generate_suggestion("grammar", "   ")

    def test_unknown_action_raises_value_error(self):
        """Unknown action raises ValueError."""
        with pytest.raises(ValueError, match="Action not available"):
            generate_suggestion("unknown_action", "hello")

    @patch("backend.services.generator.generate")
    def test_returns_suggestion_list(self, mock_generate):
        """Returns a list with one string element."""
        mock_generate.return_value = "corrected text"
        result = generate_suggestion("grammar", "hello world")
        assert result == ["corrected text"]

    @patch("backend.services.generator.generate")
    def test_calls_generate_with_prompt(self, mock_generate):
        """generate() is called with the built prompt string."""
        mock_generate.return_value = "rewritten"
        generate_suggestion("rewrite", "original text")
        # The prompt builder is called first, then generate() with that prompt
        mock_generate.assert_called_once()
        call_args = mock_generate.call_args[0][0]
        assert "original text" in call_args

    @patch("backend.services.generator.generate")
    def test_grammar_action_calls_grammar_prompt(self, mock_generate):
        """Grammar action uses the grammar prompt builder."""
        mock_generate.return_value = "fixed"
        generate_suggestion("grammar", "teh quik brown")
        call_args = mock_generate.call_args[0][0]
        assert "teh quik brown" in call_args

    @patch("backend.services.generator.generate")
    def test_rewrite_action_calls_rewrite_prompt(self, mock_generate):
        """Rewrite action uses the rewrite prompt builder."""
        mock_generate.return_value = "rewritten"
        generate_suggestion("rewrite", "quick brown fox")
        call_args = mock_generate.call_args[0][0]
        assert "quick brown fox" in call_args

    @patch("backend.services.generator.generate")
    def test_professional_action_calls_professional_prompt(self, mock_generate):
        """Professional action uses the professional prompt builder."""
        mock_generate.return_value = "professional text"
        generate_suggestion("professional", "hey what's up")
        call_args = mock_generate.call_args[0][0]
        assert "hey what's up" in call_args

    @patch("backend.services.generator.generate")
    def test_generate_exception_propagates(self, mock_generate):
        """If generate() raises, the exception propagates."""
        mock_generate.side_effect = Exception("LLM error")
        with pytest.raises(Exception, match="LLM error"):
            generate_suggestion("grammar", "hello")
