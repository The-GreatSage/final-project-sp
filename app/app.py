# app.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()

ALPHA_ENDPOINT = "https://www.alphavantage.co/query"

def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)
    if testing:
        app.config["TESTING"] = True

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/api/price")
    def api_price():
        symbol = (request.args.get("ticker") or "").upper()
        if not symbol:
            return jsonify({"error": "ticker is required"}), 400

        # In tests (or if no key), return deterministic fake data—no network needed.
        if testing or not os.getenv("ALPHA_VANTAGE_API_KEY"):
            return jsonify({
                "meta": {"symbol": symbol},
                "series": [
                    {"timestamp": "2025-08-08 00:00:00", "close": 100.0},
                    {"timestamp": "2025-08-11 00:00:00", "close": 101.5},
                    {"timestamp": "2025-08-12 00:00:00", "close": 102.2},
                ],
            })

        # Real call (used in local dev with a key)
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "outputsize": "compact",
            "apikey": os.environ["ALPHA_VANTAGE_API_KEY"],
        }
        r = requests.get(ALPHA_ENDPOINT, params=params, timeout=15)
        r.raise_for_status()
        payload = r.json()
        ts = payload.get("Time Series (Daily)", {})
        series = [
            {"timestamp": f"{d} 00:00:00", "close": float(v["4. close"])}
            for d, v in sorted(ts.items())
        ]
        return jsonify({"meta": {"symbol": symbol}, "series": series})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=True)
