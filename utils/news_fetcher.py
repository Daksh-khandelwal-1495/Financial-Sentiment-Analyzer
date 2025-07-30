import requests
import streamlit as st

@st.cache_data(show_spinner="📰 Fetching latest news...", ttl=600)
def fetch_news_via_serpapi(query, api_key, num_results=5):
    try:
        search_query = f"{query} stock"
        print(f"🔍 Querying news for: {search_query}")

        params = {
            "q": search_query,
            "api_key": api_key,
            "engine": "google_news",  # ✅ Correct engine for news
            "hl": "en",
            "gl": "in"
        }

        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        print("📦 Raw SERPAPI response keys:", list(data.keys()))

        articles = []
        news_results = data.get("news_results")
        if news_results:
            for item in news_results[:num_results]:
                if "title" in item:
                    articles.append(item["title"])
        else:
            print(f"⚠️ No 'news_results' found in SerpAPI response for: {query}")

        return articles

    except Exception as e:
        print(f"❌ Error fetching news for {query}: {e}")
        return []
