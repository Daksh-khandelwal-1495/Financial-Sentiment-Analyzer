from textblob import TextBlob

# Sample headlines
headlines = [
    "TCS posts record profit in Q1, shares likely to surge",
    "TCS faces legal trouble in overseas market",
    "TCS announces partnership with European fintech",
    "Tech sector sees a dip, TCS among the biggest losers",
    "TCS expands hiring for AI and cloud services"
]

print("📊 Sentiment Analysis of Headlines:\n")
for headline in headlines:
    blob = TextBlob(headline)
    sentiment_score = blob.sentiment.polarity
    print(f"📰 {headline}")
    print(f"   ➤ Sentiment Score: {sentiment_score:.2f}\n")
