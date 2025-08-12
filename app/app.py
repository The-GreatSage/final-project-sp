from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from .cache import get_stock_data # The relative import is still correct

def create_app():
    """Create and configure an instance of the Flask application."""
    # Load environment variables from .env file
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
            return {"error": "Please provide a ticker"}, 400

        # get_stock_data returns a tuple on error, and a dict on success
        result = get_stock_data(ticker, interval="DAILY", range_="1mo")

        # Check if the result is a tuple, which indicates an error
        if isinstance(result, tuple):
            # It's an error, so unpack the tuple and return the parts
            error_body, status_code = result
            return error_body, status_code

    @app.route("/health")
    def health():
        """Check if the app is running."""
        return {"status": "ok"}  # Simple health check

    return app
