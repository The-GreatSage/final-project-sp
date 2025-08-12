import os
import pytest

# Ensure the Flask app can be imported
from app.app import app as flask_app

@pytest.fixture(autouse=True)
def _set_test_env(monkeypatch):
    """
    Set a dummy API key for tests by default.
    Individual tests can override or delete it if needed.
    """
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "test-key")

@pytest.fixture
def client():
    """
    Give each test a Flask test client.
    """
    flask_app.config.update(TESTING=True)
    with flask_app.test_client() as c:
        yield c
