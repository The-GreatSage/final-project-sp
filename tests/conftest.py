# tests/conftest.py
import pytest
from app import app as flask_app

@pytest.fixture
def client():
    return flask_app.test_client()

