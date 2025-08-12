import os
import importlib
import pytest

# Safe dummy key for tests; your tests monkeypatch requests.get anyway
os.environ.setdefault("ALPHA_VANTAGE_API_KEY", "test_dummy_key")

# Import the installed package 'app' (repo root added via pytest.ini)
pkg = importlib.import_module("app")

# Prefer a factory if available
if hasattr(pkg, "create_app"):
    create_app = pkg.create_app
else:
    # fallback to app.app:app if you expose a module-level Flask app there
    from app.app import app as _global_app  # type: ignore

@pytest.fixture
def app():
    if 'create_app' in globals():
        return create_app(testing=True)
    return _global_app  # pragma: no cover

@pytest.fixture
def client(app):
    return app.test_client()
