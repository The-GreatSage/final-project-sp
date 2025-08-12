from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from .cache import get_stock_data
from .exceptions import ApiError

def create_app():
    """Create and configure an instance of the Flask application."""
    load_dotenv()
    app = Flask(__name__)

    @app.route("/")
    def index():
        """Show a webpage where users can enter a stock ticker."""
        return render_template("index.html")

    @app.route("/api/price")
    def api_price():
        """Get stock prices for a ticker (e.g., AAPL)."""
        ticker = request.args.get("ticker")
        if not ticker:
            # Use jsonify for consistent JSON responses
            return jsonify({"error": "Please provide a ticker"}), 400
        
        try:
            data = get_stock_data(ticker, interval="DAILY", range_="1mo")
            return jsonify(data)
        except ApiError as e:
            # Catch our custom error and return a 500 server error
            app.logger.error(f"API Error: {e}") # Good practice to log errors
            return jsonify({"error": "Failed to fetch data from external API"}), 500

    @app.route("/health")
    def health():
        """Check if the app is running."""
        return jsonify({"status": "ok"})

    return app