from flask import Flask, request, jsonify
import os, requests
from .cache import get_stock_data  # Changed to app.cache


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

        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            # tests that want to mock requests will still set a dummy key
            return jsonify({"error": "missing API key"}), 400

        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "outputsize": "compact",
            "apikey": api_key,
        }
        try:
            r = requests.get(ALPHA_ENDPOINT, params=params, timeout=15)
            r.raise_for_status()
            payload = r.json()
        except requests.RequestException as e:
            # upstream/network problem
            return jsonify({"error": "upstream_error", "detail": str(e)}), 502

        # Alpha Vantage error/rate-limit formats
        err_detail = payload.get("Error Message") or payload.get("Note") or payload.get("Information")
        if err_detail:
            return jsonify({"error": "alpha_vantage_error", "detail": err_detail}), 400

        ts = payload.get("Time Series (Daily)")
        if not ts:
            # unexpected shape from provider
            return jsonify({"error": "no_time_series"}), 502

        series = [
            {"timestamp": f"{d} 00:00:00", "close": float(v["4. close"])}
            for d, v in sorted(ts.items())
        ]
        return jsonify({"meta": {"symbol": symbol}, "series": series})

    return app