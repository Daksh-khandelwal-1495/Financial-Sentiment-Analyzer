import yfinance as yf

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)

    info = stock.info

    print(f"🔹 Company: {info.get('longName')}")
    print(f"🔹 Sector: {info.get('sector')}")
    print(f"🔹 Industry: {info.get('industry')}")
    print(f"🔹 Market Cap: {info.get('marketCap')}")
    print(f"🔹 Forward P/E: {info.get('forwardPE')}")
    print(f"🔹 Dividend Yield: {info.get('dividendYield')}")
    print(f"\n📄 Summary:\n{info.get('longBusinessSummary')[:500]}...")

    # Last 5 days close prices
    hist = stock.history(period="5d")
    print("\n📈 Last 5 Days Closing Prices:")
    print(hist['Close'])

# Example usage
if __name__ == "__main__":
    get_stock_info("RELIANCE.NS")  # Try others: AAPL, TCS.NS, TSLA, INFY.NS
