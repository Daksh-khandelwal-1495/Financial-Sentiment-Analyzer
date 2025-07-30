# demo_scripts/pipeline_news_sentiment.py

from dotenv import load_dotenv
import os

from utils.news_fetcher import fetch_news_via_serpapi
from models.finbert_sentiment import analyze_sentiment
from utils.company_info import get_company_info

# Load environment variables (like SERPAPI_KEY)
load_dotenv()

def run_pipeline():
    print("📡 Financial Sentiment Analyzer (News-based)")
    query = input("Enter a company name or stock (e.g., 'TCS', 'Tesla', 'Reliance'): ").strip().upper()

    # 🏢 Fetch company info
    print("\n🏢 Fetching company profile...")
    try:
        company_info = get_company_info(query)

        print(f"\n📄 Company Profile")
        print(f"🔹 Name       : {company_info['name']}")
        print(f"🔹 Sector     : {company_info['sector']}")
        print(f"🔹 Industry   : {company_info['industry']}")
        print(f"🔹 Market Cap : ₹{company_info['market_cap']}")
        print(f"🔹 Price      : ₹{company_info['current_price']} ({round(company_info['day_change'] * 100, 2)}%)")
        print(f"🔹 Volume     : {company_info['volume']}")
        print(f"🔹 Earnings   : {company_info['earnings_date']}")
        print(f"🔹 Summary    : {company_info['summary'][:300]}...\n")
    
    except Exception as e:
        print(f"⚠️ Could not fetch company info: {e}")

    # 📰 Fetch news headlines
    print(f"📰 Fetching news for: {query}")
    api_key = os.getenv("SERPAPI_KEY")
    headlines = fetch_news_via_serpapi(query, api_key, num_results=5)

    if not headlines:
        print("❌ No news found.")
        return

    # 🧠 Analyze sentiment of each headline
    sentiments = []
    for idx, headline in enumerate(headlines, start=1):
        print(f"\n{idx}. 📰 Headline: {headline}")
        sentiment = analyze_sentiment(headline)
        print(f"   → Sentiment: {sentiment['label']} ({round(sentiment['score'], 2)})")
        sentiments.append(sentiment['label'])

    # 📊 Print summary
    print("\n📊 News Sentiment Summary:")
    print(f"✅ Positive: {sentiments.count('Positive')}")
    print(f"😐 Neutral : {sentiments.count('Neutral')}")
    print(f"⚠️ Negative: {sentiments.count('Negative')}")

if __name__ == "__main__":
    run_pipeline()
