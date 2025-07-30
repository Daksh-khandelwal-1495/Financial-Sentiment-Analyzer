# Financial Sentiment Analyzer 🧠📊

A Streamlit-based tool to analyze stock sentiment using FinBERT and live news from SerpAPI.

## Features
- Sector-aware company recognition (Indian + US tickers)
- Live news fetching with caching
- FinBERT-based sentiment classification
- Interactive visualizations with Plotly

## Setup
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run streamlit_app.py
