"""Unit tests for the config module (mocked environment variables)."""

import pytest
from unittest.mock import patch

class TestConfigDefaults:
    """Tests for default config values when no env vars are set."""

    @patch.dict("os.environ", {}, clear=True)
    def test_ollama_url_default(self):
        """OLLAMA_URL defaults to localhost:11434."""
        import importlib
        import backend.config as config
        importlib.reload(config)
        assert config.OLLAMA_URL == "http://localhost:11434/api/generate"

    @patch.dict("os.environ", {}, clear=True)
    def test_ollama_model_default(self):
        """OLLAMA_MODEL defaults to gemma3:4b."""
        import importlib
        import backend.config as config
        importlib.reload(config)
        assert config.OLLAMA_MODEL == "gemma3:4b"

    @patch.dict("os.environ", {}, clear=True)
    def test_llm_url_default(self):
        """LLM_URL defaults to a valid URL when no .env.server overrides it."""
        import importlib
        import backend.config as config
        importlib.reload(config)
        # Note: .env.server may override this, so we just verify it's a valid URL
        assert config.LLM_URL.startswith("https://")

    @patch.dict("os.environ", {}, clear=True)
    def test_llm_model_default(self):
        """LLM_MODEL defaults to a non-empty string when no .env.server overrides it."""
        import importlib
        import backend.config as config
        importlib.reload(config)
        # Note: .env.server may override this, so we just verify it's a non-empty string
        assert isinstance(config.LLM_MODEL, str) and len(config.LLM_MODEL) > 0

    @patch.dict("os.environ", {}, clear=True)
    def test_llm_key_is_string_or_none(self):
        """LLM_KEY is a string when configured, or None when not."""
        import importlib
        import backend.config as config
        importlib.reload(config)
        assert config.LLM_KEY is None or isinstance(config.LLM_KEY, str)

class TestConfigOverrides:
    """Tests for config values when env vars are set."""

    @patch.dict("os.environ", {
        "OLLAMA_URL": "http://custom:11434/api/generate",
        "OLLAMA_MODEL": "custom-model",
        "LLM_URL": "http://custom-server:8080/chat",
        "LLM_MODEL": "CustomModel",
        "LLM_KEY": "custom-key-123",
    })
    def test_ollama_url_overridden(self):
        import importlib
        import backend.config as config
        importlib.reload(config)
        assert config.OLLAMA_URL == "http://custom:11434/api/generate"

    @patch.dict("os.environ", {
        "OLLAMA_URL": "http://custom:11434/api/generate",
        "OLLAMA_MODEL": "custom-model",
        "LLM_URL": "http://custom-server:8080/chat",
        "LLM_MODEL": "CustomModel",
        "LLM_KEY": "custom-key-123",
    })
    def test_ollama_model_overridden(self):
        import importlib
        import backend.config as config
        importlib.reload(config)
        assert config.OLLAMA_MODEL == "custom-model"

    @patch.dict("os.environ", {
        "OLLAMA_URL": "http://custom:11434/api/generate",
        "OLLAMA_MODEL": "custom-model",
        "LLM_URL": "http://custom-server:8080/chat",
        "LLM_MODEL": "CustomModel",
        "LLM_KEY": "custom-key-123",
    })
    def test_llm_url_overridden(self):
        import importlib
        import backend.config as config
        importlib.reload(config)
        assert config.LLM_URL == "http://custom-server:8080/chat"

    @patch.dict("os.environ", {
        "OLLAMA_URL": "http://custom:11434/api/generate",
        "OLLAMA_MODEL": "custom-model",
        "LLM_URL": "http://custom-server:8080/chat",
        "LLM_MODEL": "CustomModel",
        "LLM_KEY": "custom-key-123",
    })
    def test_llm_model_overridden(self):
        import importlib
        import backend.config as config
        importlib.reload(config)
        assert config.LLM_MODEL == "CustomModel"

    @patch.dict("os.environ", {
        "OLLAMA_URL": "http://custom:11434/api/generate",
        "OLLAMA_MODEL": "custom-model",
        "LLM_URL": "http://custom-server:8080/chat",
        "LLM_MODEL": "CustomModel",
        "LLM_KEY": "custom-key-123",
    })
    def test_llm_key_overridden(self):
        import importlib
        import backend.config as config
        importlib.reload(config)
        assert config.LLM_KEY == "custom-key-123"
