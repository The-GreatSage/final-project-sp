# final-project-sp
Stock Tracker web app for Programming in Python &amp; Foundational of Software Development

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



### 0) Clone and enter the project
```bash
# in Git Bash
git clone <https://github.com/The-GreatSage/final-project-sp> stock-tracker
cd stock-tracker