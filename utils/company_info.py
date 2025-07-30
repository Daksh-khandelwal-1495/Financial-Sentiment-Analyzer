# utils/company_info.py

import yfinance as yf
import requests
import streamlit as st

# Optional: Custom ticker map
CUSTOM_TICKER_MAP = {
    "TCS": "TCS.NS",
    "INFY": "INFY.NS",
    "RELIANCE": "RELIANCE.NS",
    "WIPRO": "WIPRO.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "GOOGLE": "GOOG",
    "ALPHABET": "GOOG",
    "TESLA": "TSLA",
    "APPLE": "AAPL",
    "NVIDIA": "NVDA"
}

@st.cache_data(show_spinner="📦 Fetching company data...", ttl=3600)
def get_company_info(query):
    query_upper = query.upper()

    # 1. Check custom map
    ticker = CUSTOM_TICKER_MAP.get(query_upper)

    # 2. Search Yahoo Finance if not mapped
    if not ticker:
        print(f"🔍 '{query}' not found in map. Trying Yahoo Finance search API...")
        try:
            response = requests.get(f"https://query2.finance.yahoo.com/v1/finance/search?q={query_upper}")
            if response.status_code == 200:
                data = response.json()
                quotes = data.get("quotes", [])
                if quotes and quotes[0].get("symbol"):
                    ticker = quotes[0]["symbol"]
                else:
                    print(f"❌ No ticker found for '{query}'. It may be a private or unlisted company.")
                    return None
            else:
                print(f"❌ Yahoo Finance API request failed. Status: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error querying Yahoo Finance: {e}")
            return None

    # 3. Fetch data from yfinance
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or "shortName" not in info:
            print(f"❌ No info found for ticker '{ticker}'")
            return None

        return {
            "ticker": ticker,
            "name": info.get("shortName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "current_price": info.get("currentPrice", "N/A"),
            "day_change": info.get("regularMarketChangePercent", "N/A"),
            "volume": info.get("volume", "N/A"),
            "summary": info.get("longBusinessSummary", "N/A"),
            "earnings_date": info.get("earningsDate", "N/A"),
        }

    except Exception as e:
        print(f"❌ Failed to fetch info for ticker '{ticker}': {e}")
        return None
