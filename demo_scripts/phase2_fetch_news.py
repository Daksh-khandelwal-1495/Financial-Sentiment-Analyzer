import feedparser

def get_news_headlines(query, max_results=10):
    query = query.replace(" ", "+")  # URL-safe
    rss_url = f"https://news.google.com/rss/search?q={query}"

    feed = feedparser.parse(rss_url)

    print(f"\n📰 Top {max_results} headlines for '{query.replace('+', ' ')}':\n")

    headlines = []
    for entry in feed.entries[:max_results]:
        print(f"• {entry.title}")
        print(f"  {entry.link}\n")
        headlines.append({
            'title': entry.title,
            'link': entry.link
        })

    return headlines

# Example usage
if __name__ == "__main__":
    get_news_headlines("TCS")  # or TATA Steel, INFY, AAPL
