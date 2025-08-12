from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from app.cache import get_stock_data  # Changed to app.cache

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)  # Create the Flask app

@app.route("/")
def index():
    """Show a webpage where users can enter a stock ticker."""
    return render_template("index.html")

@app.route("/api/price")
def api_price():
    """Get stock prices for a ticker (e.g., AAPL)."""
    ticker = request.args.get("ticker")  # Get ticker from URL (e.g., ?ticker=AAPL)
    if not ticker:
        return {"error": "Please provide a ticker"}, 400  # Error if no ticker
    data = get_stock_data(ticker, interval="DAILY", range_="1mo")  # Get data from cache.py
    if "error" in data:
        return data, 500  # Return error if API fails
    return data  # Return stock data as JSON

@app.route("/health")
def health():
    """Check if the app is running."""
    return {"status": "ok"}  # Simple health check