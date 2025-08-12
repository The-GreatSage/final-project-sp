import pytest

def test_api_no_ticker(client):
    """Test API returns error if no ticker is provided."""
    response = client.get("/api/price")
    assert response.status_code == 400
    assert response.json == {"error": "Please provide a ticker"}

def test_api_valid_ticker(monkeypatch, client):
    """Test API returns stock data for a valid ticker."""
    fake_data = {"Time Series (Daily)": {"2025-08-01": {"4. close": "150.00"}}}
    def mock_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                return fake_data
        return MockResponse()
    monkeypatch.setattr("app.cache.requests.get", mock_get)
    response = client.get("/api/price?ticker=AAPL")
    assert response.status_code == 200
    assert response.json == fake_data

def test_api_invalid_key(monkeypatch, client):
    """Test API handles invalid API key."""
    def mock_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                return {"Error Message": "Invalid API key"}
        return MockResponse()
    monkeypatch.setattr("app.cache.requests.get", mock_get)
    response = client.get("/api/price?ticker=AAPL")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid ticker or API key"}