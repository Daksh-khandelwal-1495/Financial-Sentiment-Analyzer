import requests
from bs4 import BeautifulSoup
from newspaper import Article

def extract_article_text(google_news_url: str) -> str:
    try:
        # Resolve Google redirect
        response = requests.get(google_news_url, allow_redirects=True, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        final_url = response.url

        # First try: newspaper3k
        try:
            article = Article(final_url)
            article.download()
            article.parse()
            if article.text.strip():
                return article.text.strip()
        except:
            pass

        # Fallback: BeautifulSoup
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)
        return text.strip()

    except Exception as e:
        print(f"❌ Error extracting article: {e}")
        return ""
