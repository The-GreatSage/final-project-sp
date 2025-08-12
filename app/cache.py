import requests
from dotenv import load_dotenv
import os
import time
from .exceptions import ApiError  # Import our custom exception

# Load environment variables
load_dotenv()
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
CACHE = {}
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", 120))

def get_stock_data(ticker, interval, range_):
    """
    Fetch stock data from Alpha Vantage or cache.
    Raises ApiError on failure.
    """
    cache_key = f"{ticker}_{interval}_{range_}"
    if cache_key in CACHE and time.time() - CACHE[cache_key]["time"] < CACHE_TTL:
        return CACHE[cache_key]["data"]
    
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_{interval}&symbol={ticker}&apikey={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        
        # Alpha Vantage sometimes returns errors in a 200 OK response body
        if "Error Message" in data:
            raise ApiError(f"Alpha Vantage API error: {data['Error Message']}")
            
        CACHE[cache_key] = {"data": data, "time": time.time()}
        return data
        
    except requests.exceptions.RequestException as e:
        # Handle network errors (e.g., connection timeout)
        raise ApiError(f"Network error fetching data for {ticker}: {e}")
    except ValueError:
        # Handle errors if the response is not valid JSON
        raise ApiError(f"Failed to decode JSON response for {ticker}")