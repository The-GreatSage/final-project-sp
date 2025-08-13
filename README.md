# Stock Tracker Web App

A simple web app to view stock price charts using Alpha Vantage and Chart.js.

## Features
- Enter a stock ticker (e.g., AAPL) to see a price chart.
- Uses a cache to avoid extra API calls.
- No database or login needed.
- Tests with pytest and automatic testing with GitHub Actions.

## Setup
1. **Clone the Project**:
   ```bash
   git clone https://github.com/The-GreatSage/final-project-sp
   cd final-project-sp


Create a Conda Environment:
conda create -n env-name python=3.11
conda activate env-name


Install Packages:
pip install -r requirements.txt


Set Up API Key:

Open .env in a text editor and add your Alpha Vantage API key:ALPHAVANTAGE_API_KEY=your_real_key_here
CACHE_TTL_SECONDS=120

Get a free API key from Alpha Vantage.

Run the App:
python -m app.app

Open http://localhost:8000 in your browser and enter a ticker (e.g., AAPL).

Run Tests:
pytest -vv -m "not integration"

Tests check the API and health endpoint without real API calls.

License
This project uses the MIT License. See LICENSE for details.```