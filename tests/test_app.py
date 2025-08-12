def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"ok": True}

def test_api_requires_symbol(client):
    r = client.get("/api/price")  # no ?symbol=
    assert r.status_code == 400
    data = r.get_json()
    assert "error" in data

def test_api_returns_data_and_caches(monkeypatch, client):
    # Fake the Alpha Vantage function to avoid network calls
    from app import services

    def fake_fetch_daily_adjusted(symbol, api_key):
        return [
            {"date": "2024-12-30", "close": 100.0},
            {"date": "2024-12-31", "close": 101.5},
            {"date": "2025-01-02", "close": 102.0},
        ]

    # Replace the real function with our fake one for this test
    monkeypatch.setattr(services.alpha_vantage, "fetch_daily_adjusted", fake_fetch_daily_adjusted)

    # First call -> not cached
    r1 = client.get("/api/price?symbol=AAPL")
    assert r1.status_code == 200
    data1 = r1.get_json()
    assert data1["symbol"] == "AAPL"
    assert data1["cached"] is False
    assert len(data1["series"]) == 3

    # Second call -> should be cached
    r2 = client.get("/api/price?symbol=AAPL")
    assert r2.status_code == 200
    data2 = r2.get_json()
    assert data2["cached"] is True
    assert data2["series"] == data1["series"]  # same data

def test_api_missing_api_key(monkeypatch, client):
    # Remove the API key for this test to trigger the 500 path
    monkeypatch.delenv("ALPHAVANTAGE_API_KEY", raising=False)
    r = client.get("/api/price?symbol=MSFT")
    assert r.status_code == 500
    assert "error" in r.get_json()
