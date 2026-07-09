"""Unit tests for the LLM client (mocked requests)."""

import pytest
from unittest.mock import patch, MagicMock

from backend.services.llm import generate

class TestLlmClientOpenAIServer:
    """Tests for the OpenAI-compatible server path (when LLM_KEY is set)."""

    @patch("backend.services.llm.requests.post")
    def test_returns_content_from_openai_server(self, mock_post):
        """Returns the content from the first choice's message."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "generated text"}}]
        }
        mock_post.return_value = mock_response
        result = generate("test prompt")
        assert result == "generated text"

    @patch("backend.services.llm.requests.post")
    def test_sends_correct_payload_to_openai_server(self, mock_post):
        """Sends the correct JSON payload with model, messages, and content."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "hi"}}]
        }
        mock_post.return_value = mock_response
        generate("test prompt")
        call_args = mock_post.call_args
        payload = call_args[1]["json"]
        assert "model" in payload
        assert "messages" in payload
        assert payload["messages"][0]["role"] == "user"
        assert payload["messages"][0]["content"] == "test prompt"

    @patch("backend.services.llm.requests.post")
    def test_sends_authorization_header(self, mock_post):
        """Sends Bearer token in Authorization header."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "hi"}}]
        }
        mock_post.return_value = mock_response
        generate("test prompt")
        headers = mock_post.call_args[1]["headers"]
        assert "Authorization" in headers
        assert "Bearer" in headers["Authorization"]

    @patch("backend.services.llm.requests.post")
    def test_raises_on_server_error(self, mock_post):
        """Raises exception when server returns non-2xx status."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("500 Internal Server Error")
        mock_post.return_value = mock_response
        with pytest.raises(Exception, match="500"):
            generate("test prompt")

    @patch("backend.services.llm.requests.post")
    def test_raises_on_missing_choices(self, mock_post):
        """Raises exception when response has no choices."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": []}
        mock_post.return_value = mock_response
        with pytest.raises(IndexError):
            generate("test prompt")

    @patch("backend.services.llm.requests.post")
    def test_raises_on_missing_message_key(self, mock_post):
        """Raises exception when choice has no message key."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": [{}]}
        mock_post.return_value = mock_response
        with pytest.raises(KeyError):
            generate("test prompt")

    @patch("backend.services.llm.requests.post")
    def test_raises_on_missing_content_key(self, mock_post):
        """Raises exception when message has no content key."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": [{"message": {}}]}
        mock_post.return_value = mock_response
        with pytest.raises(KeyError):
            generate("test prompt")

class TestLlmClientOllamaFallback:
    """Tests for the Ollama local fallback path (when LLM_KEY is not set)."""

    @patch("backend.services.llm.requests.post")
    def test_returns_ollama_response(self, mock_post):
        """Returns the response from Ollama when LLM_KEY is not set."""
        with patch("backend.services.llm.LLM_KEY", None):
            mock_response = MagicMock()
            mock_response.json.return_value = {"response": "ollama text"}
            mock_post.return_value = mock_response
            result = generate("test prompt")
            assert result == "ollama text"

    @patch("backend.services.llm.requests.post")
    def test_sends_ollama_payload(self, mock_post):
        """Sends the correct Ollama payload with model, prompt, and stream."""
        with patch("backend.services.llm.LLM_KEY", None):
            mock_response = MagicMock()
            mock_response.json.return_value = {"response": "ollama text"}
            mock_post.return_value = mock_response
            generate("test prompt")
            call_args = mock_post.call_args
            payload = call_args[1]["json"]
            assert "model" in payload
            assert "prompt" in payload
            assert payload["prompt"] == "test prompt"
            assert payload["stream"] is False

    @patch("backend.services.llm.requests.post")
    def test_raises_on_ollama_missing_response_key(self, mock_post):
        """Raises exception when Ollama response has no 'response' key."""
        with patch("backend.services.llm.LLM_KEY", None):
            mock_response = MagicMock()
            mock_response.json.return_value = {}
            mock_post.return_value = mock_response
            with pytest.raises(KeyError):
                generate("test prompt")
