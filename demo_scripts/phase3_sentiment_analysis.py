from transformers import pipeline
from newspaper import Article
import time

# Load FinBERT pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def analyze_article_sentiment(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        text = article.text

        if len(text.strip()) == 0:
            print(f"❌ Empty article at: {url}")
            return None

        result = sentiment_pipeline(text[:512])  # FinBERT takes max 512 tokens
        print(f"\n📰 Article: {article.title}")
        print(f"📌 URL: {url}")
        print(f"🧠 Sentiment: {result[0]['label']} (Score: {round(result[0]['score'], 3)})\n")

        return {
            'title': article.title,
            'url': url,
            'sentiment': result[0]['label'],
            'confidence': round(result[0]['score'], 3)
        }

    except Exception as e:
        print(f"⚠️ Failed to process {url}: {e}")
        return None

# Test it out with a sample news URL
if __name__ == "__main__":
    sample_url = "https://www.moneycontrol.com/news/business/reliance-industries-q1-net-profit-jumps-10-1-yoy-to-rs-19399-crore-beats-estimates-13105981.html"
    analyze_article_sentiment(sample_url)
