import requests
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")  # Get API key from .env
CACHE = {}  # Store data in memory
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", 120))  # Cache for 2 minutes

def get_stock_data(ticker, interval, range_):
    """Fetch stock data from Alpha Vantage or cache."""
    cache_key = f"{ticker}_{interval}_{range_}"
    if cache_key in CACHE and time.time() - CACHE[cache_key]["time"] < CACHE_TTL:
        return CACHE[cache_key]["data"]
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_{interval}&symbol={ticker}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if "Error Message" in data:
            return {"error": "Invalid ticker or API key"}, 400
        
        CACHE[cache_key] = {"data": data, "time": time.time()}
    
        return data
        
    except Exception:
        return {"error": "Failed to fetch data"}, 500