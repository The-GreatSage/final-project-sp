# tests/conftest.py
import os
import sys
import importlib.util
import pytest

# Ensure a dummy key so code paths that check for it won't crash
os.environ.setdefault("ALPHA_VANTAGE_API_KEY", "test_dummy_key")

# Load app.py from repo root without relying on packages/PYTHONPATH
ROOT = os.path.dirname(os.path.dirname(__file__))
APP_PATH = os.path.join(ROOT, "app.py")

spec = importlib.util.spec_from_file_location("app_module", APP_PATH)
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

@pytest.fixture
def flask_app():
    # Testing=True ensures the endpoint returns deterministic fake data
    return app_module.create_app(testing=True)

@pytest.fixture
def client(flask_app):
    return flask_app.test_client()
