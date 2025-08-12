from app.services.alpha_vantage import fetch_daily_adjusted

class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

def test_fetch_daily_adjusted_parses_json(monkeypatch):
    # Minimal valid Alpha Vantage-like payload
    sample_json = {
        "Time Series (Daily)": {
            "2025-01-02": {"4. close": "102.00"},
            "2024-12-31": {"4. close": "101.50"},
            "2024-12-30": {"4. close": "100.00"},
        }
    }

    def fake_get(url, params=None, timeout=10):
        return DummyResponse(sample_json)

    # Monkeypatch requests.get used inside the service
    import app.services.alpha_vantage as svc
    monkeypatch.setattr(svc.requests, "get", fake_get)

    data = fetch_daily_adjusted("AAPL", "dummy-key")
    # Should be sorted oldest -> newest
    assert data == [
        {"date": "2024-12-30", "close": 100.0},
        {"date": "2024-12-31", "close": 101.5},
        {"date": "2025-01-02", "close": 102.0},
    ]
