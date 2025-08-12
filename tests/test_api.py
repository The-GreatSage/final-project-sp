import pytest
from app.exceptions import ApiError

def test_api_no_ticker(client):
    """Test that the API returns a 400 error if no ticker is provided."""
    response = client.get("/api/price")
    assert response.status_code == 400
    assert response.json == {"error": "Please provide a ticker"}

def test_api_success(monkeypatch, client):
    """Test a successful API call."""
    fake_data = {"Time Series (Daily)": {"2025-08-01": {"4. close": "150.00"}}}
    
    # Mock the data layer function directly to return the fake data
    monkeypatch.setattr("app.app.get_stock_data", lambda *args, **kwargs: fake_data)
    
    response = client.get("/api/price?ticker=AAPL")
    assert response.status_code == 200
    assert response.json == fake_data

def test_api_handles_error(monkeypatch, client):
    """Test that the API gracefully handles an ApiError from the data layer."""
    # Helper function to raise the exception we want to test
    def mock_raise_api_error(*args, **kwargs):
        raise ApiError("Test error from mock")

    # Mock get_stock_data to raise the ApiError
    monkeypatch.setattr("app.app.get_stock_data", mock_raise_api_error)

    response = client.get("/api/price?ticker=FAIL")
    assert response.status_code == 500
    assert response.json == {"error": "Failed to fetch data from external API"}