import requests
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
import os
import time
from .exceptions import ApiError
from flask import Flask

# Load environment variables
load_dotenv()
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
CACHE = {}
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", 120))

def create_app():
    app = Flask(__name__)
    # ...your setup code...
    return app

def _format_yfinance_data(data: pd.DataFrame) -> dict:
    """Formats yfinance DataFrame to match Alpha Vantage's structure."""
    time_series = {}
    # yfinance returns a DataFrame. We need to convert it to the dict format.
    for date, row in data.iterrows():
        # The date needs to be formatted as YYYY-MM-DD
        date_str = date.strftime('%Y-%m-%d')
        time_series[date_str] = {
            "1. open": str(row["Open"]),
            "2. high": str(row["High"]),
            "3. low": str(row["Low"]),
            "4. close": str(row["Close"]),
            "5. volume": str(row["Volume"])
        }
    return {"Time Series (Daily)": time_series}

def _fetch_from_yfinance(ticker: str, range_: str) -> dict:
    """Fetches stock data from yfinance and formats it."""
    try:
        stock = yf.Ticker(ticker)
        # yfinance uses '1mo' for range, which is convenient
        hist = stock.history(period=range_)
        if hist.empty:
            raise ApiError(f"No data found for ticker '{ticker}' on yfinance.")
        return _format_yfinance_data(hist)
    except Exception as e:
        # Catch any other exception from yfinance and wrap it
        raise ApiError(f"yfinance failed for ticker '{ticker}': {e}")

def get_stock_data(ticker, interval, range_):
    """
    Fetch stock data from cache, Alpha Vantage, or yfinance (as a fallback).
    Raises ApiError on failure.
    """
    cache_key = f"{ticker}_{interval}_{range_}"
    if cache_key in CACHE and time.time() - CACHE[cache_key]["time"] < CACHE_TTL:
        return CACHE[cache_key]["data"]
    
    # --- Primary Source: Alpha Vantage ---
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_{interval}&symbol={ticker}&apikey={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get("Error Message") or data.get("Information"):
            # The API can return a 200 OK with an error/info message about usage limits
            error_message = data.get("Error Message", "") + data.get("Information", "")
            raise ApiError(f"Alpha Vantage API error: {error_message}")
            
        CACHE[cache_key] = {"data": data, "time": time.time()}
        return data
        
    except (requests.exceptions.RequestException, ValueError, ApiError) as e:
        # If Alpha Vantage fails for any reason, try the fallback.
        print(f"Alpha Vantage failed: {e}. Trying yfinance fallback...") # Using print for visibility on Render logs
        try:
            data = _fetch_from_yfinance(ticker, range_)
            # We can also cache the successful fallback response
            CACHE[cache_key] = {"data": data, "time": time.time()}
            return data
        except ApiError as yf_e:
            # If the fallback also fails, then we admit defeat.
            raise ApiError(f"All data sources failed. Primary: {e}. Fallback: {yf_e}")