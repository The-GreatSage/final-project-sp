import os
from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
from .services.alpha_vantage import fetch_daily_adjusted
from utils.cache import Cache

# Load environment variables from .env file
load_dotenv()

# Create a small cache to store results for a short time
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "120"))
cache = Cache(default_ttl=CACHE_TTL)

app = Flask(__name__, static_folder="static", static_url_path="/static")

@app.route("/")
def home():
    # Serve the HTML page
    return send_from_directory(app.static_folder, "index.html")

@app.route("/health")
def health():
    # Simple health check
    return jsonify({"ok": True})

@app.route("/api/price")
def api_price():
    symbol = request.args.get("symbol", "").upper().strip()

    if symbol == "":
        return jsonify({"error": "Please provide a symbol"}), 400

    # Check if data is already in cache
    cached_data = cache.get(symbol)
    if cached_data:
        return jsonify({"symbol": symbol, "series": cached_data, "cached": True})

    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        return jsonify({"error": "Missing API key"}), 500

    try:
        data = fetch_daily_adjusted(symbol, api_key)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Store in cache and return
    cache.set(symbol, data)
    return jsonify({"symbol": symbol, "series": data, "cached": False})

if __name__ == "__main__":
    app.run(port=8000, debug=True)
