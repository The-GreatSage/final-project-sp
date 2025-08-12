import requests

# Base URL for Alpha Vantage API
BASE_URL = "https://www.alphavantage.co/query"

def fetch_daily_adjusted(symbol, api_key):
    """
    Get daily adjusted stock prices from Alpha Vantage.
    Returns a list of dictionaries with date and close price.
    """
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": api_key
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    data = response.json()

    if "Error Message" in data:
        raise Exception("Invalid symbol or request error.")
    if "Time Series (Daily)" not in data:
        raise Exception("Unexpected API response.")

    time_series = data["Time Series (Daily)"]

    # Convert to list of {date, close}
    prices = []
    for date, values in time_series.items():
        prices.append({"date": date, "close": float(values["4. close"])})

    # Sort by date (oldest first)
    prices.sort(key=lambda x: x["date"])
    return prices
