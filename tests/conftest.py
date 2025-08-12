import pytest
from app import create_app  # works because pytest.ini sets pythonpath=.

@pytest.fixture
def flask_app():
    return create_app(testing=True)

@pytest.fixture
def client(flask_app):
    return flask_app.test_client()