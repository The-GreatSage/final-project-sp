import pytest

@pytest.fixture
def app():
    """
    Create and configure a new app instance for each test.
    This fixture delays the import of the app to avoid startup errors.
    """
    # Moving the import inside the fixture function is the key to the fix.
    from app.app import app
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()