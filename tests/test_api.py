import pytest
from app.exceptions import ApiError

# Sample data that mimics the Alpha Vantage structure
FAKE_SUCCESS_DATA = {"Time Series (Daily)": {"2025-08-01": {"4. close": "150.00"}}}

def test_api_no_ticker(client):
    """Test that the API returns a 400 error if no ticker is provided."""
    response = client.get("/api/price")
    assert response.status_code == 400
    assert response.json == {"error": "Please provide a ticker"}

def test_api_success_from_alphavantage(monkeypatch, client):
    """Test a successful API call using the primary data source (Alpha Vantage)."""
    monkeypatch.setattr("app.cache._fetch_from_alphavantage", lambda *args, **kwargs: FAKE_SUCCESS_DATA)
    
    response = client.get("/api/price?ticker=AAPL")
    assert response.status_code == 200
    assert response.json == FAKE_SUCCESS_DATA

def test_api_fallback_to_yfinance(monkeypatch, client):
    """Test that the API gracefully falls back to yfinance when Alpha Vantage fails."""
    def mock_raise_av_error(*args, **kwargs):
        raise ApiError("Alpha Vantage is down")
    monkeypatch.setattr("app.cache._fetch_from_alphavantage", mock_raise_av_error)
    
    monkeypatch.setattr("app.cache._fetch_from_yfinance", lambda *args, **kwargs: FAKE_SUCCESS_DATA)

    response = client.get("/api/price?ticker=GOOG")
    assert response.status_code == 200
    assert response.json == FAKE_SUCCESS_DATA

def test_api_all_sources_fail(monkeypatch, client):
    """Test that the API returns a 500 error when all data sources fail."""
    def mock_raise_av_error(*args, **kwargs):
        raise ApiError("Alpha Vantage is down")
    monkeypatch.setattr("app.cache._fetch_from_alphavantage", mock_raise_av_error)

    def mock_raise_yf_error(*args, **kwargs):
        raise ApiError("yfinance is down")
    monkeypatch.setattr("app.cache._fetch_from_yfinance", mock_raise_yf_error)

    response = client.get("/api/price?ticker=FAIL")
    assert response.status_code == 500
    assert response.json == {"error": "Failed to fetch data from external API"}