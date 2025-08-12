# app/app.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# IMPORTANT: use package-relative imports
from .services.alpha_vantage import fetch_daily_adjusted
from .utils.cache import Cache

load_dotenv()

def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)
    if testing:
        app.config["TESTING"] = True

    # tiny in-memory cache (seconds)
    ttl_seconds = int(os.getenv("CACHE_TTL_SECONDS", "120"))
    cache = Cache(default_ttl=ttl_seconds)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/api/price")
    def api_price():
        symbol = request.args.get("ticker", "").upper()
        if not symbol:
            return jsonify({"error": "ticker is required"}), 400
        # range/interval are no-ops in this simple version; Alpha Vantage uses function
        cache_key = f"price:{symbol}"
        data = cache.get(cache_key)
        if data is None:
            data = fetch_daily_adjusted(symbol)
            cache.set(cache_key, data)
        return jsonify(data)

    return app

if __name__ == "__main__":
    # allow `python -m app.app` or `python app/app.py`
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=True)
