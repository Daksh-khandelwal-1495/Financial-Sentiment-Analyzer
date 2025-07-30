# streamlit_app.py

import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
import os

from utils.company_info import get_company_info
from utils.news_fetcher import fetch_news_via_serpapi
from models.finbert_sentiment import analyze_sentiment

# Load .env variables
load_dotenv()

# Page setup
st.set_page_config(page_title="📊 JPMorgan-style Financial Sentiment Analyzer", layout="wide")
st.title("📡 Financial Sentiment Analyzer")
st.caption("by Daksh — Inspired by JPMorgan tools")

# --- Company options for autocomplete
COMPANY_OPTIONS = [
    "TCS", "Infosys", "Reliance", "Wipro", "HDFC Bank",
    "Google", "Alphabet", "Tesla", "Apple", "Nvidia",
    "Microsoft", "Amazon", "Meta", "OpenAI", "JPMorgan", "Goldman Sachs"
]

# --- Input field with autocomplete + manual entry
default = COMPANY_OPTIONS[0]
company_query = st.text_input("🔍 Enter or select a company", value=default)
st.caption("Try: TCS, Reliance, Apple, Nvidia, OpenAI, etc.")

if company_query:
    col1, col2 = st.columns([2, 3])

    # --- Company Info Section
    with col1:
        with st.expander("🏦 Company Profile", expanded=True):
            try:
                info = get_company_info(company_query.upper())
                if info is None:
                    st.warning("⚠️ Could not fetch company info. This might be an unlisted or private company.")
                else:
                    st.markdown(f"""
                        **{info['name']}**  
                        *Sector:* {info['sector']}  
                        *Industry:* {info['industry']}  
                        *Market Cap:* ₹{info['market_cap']:,}  
                        *Price:* ₹{info['current_price']} ({round(info['day_change'] * 100, 2)}%)  
                        *Volume:* {info['volume']}  
                        *Earnings Date:* {info['earnings_date']}  
                    """)
                    st.info(info['summary'][:500] + ("..." if len(info['summary']) > 500 else ""))
            except Exception as e:
                st.error(f"❌ Could not fetch company info: {e}")

    # --- News Sentiment Section
    with col2:
        with st.expander("📰 Latest News Headlines + Sentiment", expanded=True):
            api_key = os.getenv("SERPAPI_KEY")
            headlines = fetch_news_via_serpapi(company_query, api_key, num_results=5)

            if not headlines:
                st.warning("⚠️ No news articles found for this company.")
            else:
                sentiments = []
                color_map = {
                    "Positive": ("green", "📈"),
                    "Neutral": ("gray", "🔍"),
                    "Negative": ("red", "📉")
                }

                for title in headlines:
                    sentiment = analyze_sentiment(title)
                    label = sentiment['label']
                    sentiments.append(label)
                    color, emoji = color_map[label]
                    st.markdown(
                        f"<span style='color:{color}; font-weight:bold'>{emoji} {label}</span>: {title}",
                        unsafe_allow_html=True
                    )

                st.divider()

                # --- Sentiment Summary Chart
                st.subheader("📊 Sentiment Distribution")
                sentiment_counts = {
                    "Positive": sentiments.count("Positive"),
                    "Neutral": sentiments.count("Neutral"),
                    "Negative": sentiments.count("Negative")
                }
                fig = px.pie(
                    names=list(sentiment_counts.keys()),
                    values=list(sentiment_counts.values()),
                    color=list(sentiment_counts.keys()),
                    color_discrete_map={"Positive": "green", "Neutral": "gray", "Negative": "red"},
                    title="Headline Sentiment"
                )
                st.plotly_chart(fig, use_container_width=True)
                st.caption("Sentiment analysis is powered by FinBERT and reflects article tone, not stock performance.")
