# app/services/alpha_vantage.py
import os
import requests
from typing import Dict, Any, List

ALPHA_ENDPOINT = "https://www.alphavantage.co/query"

def _get_api_key() -> str:
    key = os.getenv("ALPHA_VANTAGE_API_KEY") or os.getenv("ALPHAVANTAGE_API_KEY")
    if not key:
        raise RuntimeError("Missing ALPHA_VANTAGE_API_KEY")
    return key

def fetch_daily_adjusted(symbol: str) -> Dict[str, Any]:
    """Return compact daily adjusted data as {meta, series:[{timestamp, close}...]}."""
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": _get_api_key(),
    }
    r = requests.get(ALPHA_ENDPOINT, params=params, timeout=15)
    r.raise_for_status()
    payload = r.json()
    series_key = "Time Series (Daily)"
    if series_key not in payload:
        # Normalize Alpha Vantage error messages
        return {"meta": {"symbol": symbol}, "series": []}

    rows: List[Dict[str, Any]] = []
    ts = payload[series_key]
    # newest first
    for date, row in sorted(ts.items(), key=lambda x: x[0]):
        rows.append({"timestamp": f"{date} 00:00:00", "close": float(row["4. close"])})
    return {"meta": {"symbol": symbol}, "series": rows}
