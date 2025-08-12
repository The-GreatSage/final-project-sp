# final-project-sp


# Stock Tracker Web App

Minimal stock charting app. Fetches prices from **Alpha Vantage** and renders a **Chart.js** line chart. 

## Features
- One endpoint: `GET /api/price?ticker=AAPL&interval=1day&range=1mo`
- Single provider: **Alpha Vantage** (no fallback complexity)
- Tiny in-memory TTL cache to reduce duplicate calls
- Zero database, zero authentication
- Tests with **pytest**; CI with GitHub Actions

---

## Setup (Conda + Git Bash)

```bash
git clone <your-repo-url>
cd stock-tracker

# Create environment

conda create --name stock-tracker python=3.11
conda activate stock-tracker

# Install Dependencies

pip install -r requirements.txt

# env files

# .env — contains your real API key (not committed)
ALPHAVANTAGE_API_KEY=your_real_key
CACHE_TTL_SECONDS=120
# .env.example — placeholder template (committed)
# Make sure .env is in .gitignore.

## RUN

python -m app.app

# Open http://localhost:8000 and enter a symbol like AAPL.


