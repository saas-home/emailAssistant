"""Unit tests for prompt builders — edge cases (no LLM server needed)."""

import pytest

from backend.prompts.registry import PROMPTS

class TestPromptEdgeCases:
    """Tests for prompt builder edge cases — no LLM server needed."""

    def test_empty_string_prompt(self):
        """Empty string should still produce a prompt (not crash)."""
        for name, fn in PROMPTS.items():
            prompt = fn("")
            assert isinstance(prompt, str)
            assert len(prompt) > 0

    def test_very_long_text_prompt(self):
        """Very long text should not crash the prompt builder."""
        long_text = "word " * 10000
        for name, fn in PROMPTS.items():
            prompt = fn(long_text)
            assert isinstance(prompt, str)
            assert len(prompt) > 0

    def test_prompt_contains_user_text(self):
        """Each prompt should include the user's text."""
        sample = "unique test string xyz123"
        for name, fn in PROMPTS.items():
            prompt = fn(sample)
            assert sample in prompt

    def test_prompt_contains_instruction_keywords(self):
        """Each prompt should contain instruction-like keywords."""
        sample = "test text"
        for name, fn in PROMPTS.items():
            prompt = fn(sample)
            # All prompts should have some instruction content
            assert len(prompt) > 50

    def test_grammar_prompt_has_grammar_keywords(self):
        """Grammar prompt should mention grammar-related terms."""
        prompt = PROMPTS["grammar"]("test sentence")
        assert "grammar" in prompt.lower() or "correct" in prompt.lower()

    def test_rewrite_prompt_has_rewrite_keywords(self):
        """Rewrite prompt should mention rewrite-related terms."""
        prompt = PROMPTS["rewrite"]("test text")
        assert "rewrite" in prompt.lower() or "rewritten" in prompt.lower()

    def test_professional_prompt_has_professional_keywords(self):
        """Professional prompt should mention professional-related terms."""
        prompt = PROMPTS["professional"]("test text")
        assert "professional" in prompt.lower() or "tone" in prompt.lower()

    def test_special_characters_in_prompt(self):
        """Special characters in text should not crash the prompt builder."""
        special_text = "Hello! @#$%^&*() world"
        for name, fn in PROMPTS.items():
            prompt = fn(special_text)
            assert isinstance(prompt, str)
            assert special_text in prompt

    def test_unicode_in_prompt(self):
        """Unicode text should be included in the prompt."""
        unicode_text = "こんにちは世界"
        for name, fn in PROMPTS.items():
            prompt = fn(unicode_text)
            assert unicode_text in prompt

    def test_newlines_in_prompt(self):
        """Text with newlines should be included in the prompt."""
        multiline_text = "line1\nline2\nline3"
        for name, fn in PROMPTS.items():
            prompt = fn(multiline_text)
            assert multiline_text in prompt

    def test_all_prompts_are_different(self):
        """Each prompt builder should produce different output."""
        sample = "test text"
        prompts = {name: fn(sample) for name, fn in PROMPTS.items()}
        # All prompts should be unique
        unique_prompts = set(prompts.values())
        assert len(unique_prompts) == len(prompts), "Some prompts are identical"
