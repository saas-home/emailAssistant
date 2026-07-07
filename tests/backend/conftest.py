"""Shared fixtures for backend integration tests."""

import os

from dotenv import load_dotenv

import pytest
from fastapi.testclient import TestClient

from backend.app import app

# Load the same dotenv files the backend config uses, so skip logic stays in sync
_config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "backend")
load_dotenv(os.path.join(_config_dir, ".env"))
load_dotenv(os.path.join(_config_dir, ".env.server"))


def pytest_configure(config):
    """Register custom markers used by these tests."""
    config.addinivalue_line(
        "markers",
        "available_server: tests that require the LLM server (skipped when no key/url)",
    )
    config.addinivalue_line(
        "markers",
        "no_server: tests that run without the LLM server",
    )


def _server_available() -> bool:
    """Return True when both LLM_URL and LLM_KEY are configured."""
    return bool(os.environ.get("LLM_URL") and os.environ.get("LLM_KEY"))


def pytest_runtest_setup(item):
    """Skip tests tagged ``available_server`` when the LLM server is not configured."""
    if item.get_closest_marker("available_server"):
        if not _server_available():
            pytest.skip("LLM_URL / LLM_KEY not set — server test skipped")


@pytest.fixture()
def client():
    """Provide a FastAPI TestClient for the email-assistant backend."""
    with TestClient(app) as c:
        yield c
