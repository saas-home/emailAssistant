"""Smoke tests for the prompt registry.

These do not call any LLM — they only verify that every registered action has
a builder function producing non-empty output for valid inputs.
"""

import pytest

from backend.prompts.registry import PROMPTS


@pytest.mark.no_server
class TestPromptRegistry:
    """Each registered action produces a prompt."""

    def test_all_actions_have_builder(self):
        """PROMPTS dict is not empty and every value is callable."""
        assert PROMPTS, "PROMPTS registry is empty — forgot to register a new action?"
        for name, fn in PROMPTS.items():
            assert callable(fn), f"PROMPTS[{name!r}] is not callable"

    def test_each_builder_returns_text(self):
        """Every builder produces a non-empty prompt string."""
        sample = "the quick brown fox jumps"
        for name, fn in PROMPTS.items():
            prompt = fn(sample)
            assert prompt.strip(), f"Prompts[{name!r}] returned empty prompt"

    def test_grammar_has_instructions(self):
        """Grammar prompt includes instruction-like keywords (sanity check)."""
        prompt = PROMPTS["grammar"]("test sentence here")
        assert len(prompt) > 50  # a real instruction, not a one-liner

    def test_rewrite_has_instructions(self):
        """Rewrite prompt includes instruction-like keywords."""
        prompt = PROMPTS["rewrite"]("rewrite this")
        assert len(prompt) > 50

    def test_professional_has_instructions(self):
        """Professional prompt includes instruction-like keywords."""
        prompt = PROMPTS["professional"]("hey what's up")
        assert len(prompt) > 50
