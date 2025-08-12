# tests/conftest.py
import os
import pytest

# prevent crashes when key is missing in CI
os.environ.setdefault("ALPHA_VANTAGE_API_KEY", "test_dummy_key")

from app import create_app  # pythonpath is set via pytest.ini

@pytest.fixture
def flask_app():
    return create_app(testing=True)

@pytest.fixture
def client(flask_app):
    return flask_app.test_client()
