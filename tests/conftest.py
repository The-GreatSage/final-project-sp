import pytest
from app.app import create_app
from app import cache

@pytest.fixture(autouse=True)
def clean_cache():  # <--- Add this new fixture
    """A fixture to automatically clear the cache before each test."""
    cache.CACHE.clear()

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()