# These lines let Python find and load files
import importlib.util
import sys
import os

# Find the path to app.py, which is inside the 'app' folder
# We start from where this conftest.py file is (in 'tests' folder)
# Then go up one level ("..") and into "app/app.py"
base_dir = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(base_dir, "..", "app", "app.py")

# Load app.py as a module (like including it in our code)
spec = importlib.util.spec_from_file_location("app_module", app_path)
app_module = importlib.util.module_from_spec(spec)
sys.modules["app_module"] = app_module
spec.loader.exec_module(app_module)

# This is a helper for tests (a "fixture" in pytest)
# It gives tests access to the app in app.py
import pytest
@pytest.fixture
def app():
    return app_module.app  # Assumes 'app' is the main thing in app.py (like a Flask app)