import requests
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
import os
import time
from .exceptions import ApiError

# Load environment variables
load_dotenv()
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
CACHE = {}
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", 120))

def _format_yfinance_data(data: pd.DataFrame) -> dict:
    """Formats yfinance DataFrame to match Alpha Vantage's structure."""
    time_series = {}
    for date, row in data.iterrows():
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
        hist = stock.history(period=range_)
        if hist.empty:
            raise ApiError(f"No data found for ticker '{ticker}' on yfinance.")
        return _format_yfinance_data(hist)
    except Exception as e:
        raise ApiError(f"yfinance failed for ticker '{ticker}': {e}")

def _fetch_from_alphavantage(ticker: str, interval: str) -> dict:
    """Fetches stock data from Alpha Vantage."""
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_{interval}&symbol={ticker}&apikey={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get("Error Message") or data.get("Information"):
            error_message = data.get("Error Message", "") + data.get("Information", "")
            raise ApiError(f"Alpha Vantage API error: {error_message}")
        return data
    except (requests.exceptions.RequestException, ValueError) as e:
        raise ApiError(f"Alpha Vantage request failed: {e}")

def get_stock_data(ticker, interval, range_):
    """
    Fetch stock data from cache, or from Alpha Vantage with yfinance as a fallback.
    """
    cache_key = f"{ticker}_{interval}_{range_}"
    if cache_key in CACHE and time.time() - CACHE[cache_key]["time"] < CACHE_TTL:
        return CACHE[cache_key]["data"]
    
    try:
        data = _fetch_from_alphavantage(ticker, interval)
    except ApiError as e:
        print(f"Alpha Vantage failed: {e}. Trying yfinance fallback...")
        data = _fetch_from_yfinance(ticker, range_)
    
    CACHE[cache_key] = {"data": data, "time": time.time()}
    return data