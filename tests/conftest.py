import importlib.util
import sys
import os
import pytest

# Find app.py in the 'app' folder
base_dir = os.path.dirname(os.path.abspath(__file__))  # Path to 'tests' folder
app_path = os.path.join(base_dir, "..", "app", "app.py")  # Path to app/app.py

# Load app.py
spec = importlib.util.spec_from_file_location("app_module", app_path)
app_module = importlib.util.module_from_spec(spec)
sys.modules["app_module"] = app_module
spec.loader.exec_module(app_module)

@pytest.fixture
def app():
    """Give tests access to the Flask app."""
    return app_module.app

@pytest.fixture
def client(app):
    """Give tests a way to send fake HTTP requests."""
    return app.test_client()