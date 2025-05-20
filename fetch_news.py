import feedparser
import urllib.parse

def fetch_google_news(keyword="AI", max_articles=5):
    """Fetch news articles from Google News RSS based on a keyword with URL encoding."""
    encoded_keyword = urllib.parse.quote(keyword)
    feed_url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries[:max_articles]:
        article = {
            "title": entry.title,
            "link": entry.link,
            "published": getattr(entry, "published", "Unknown"),
            "summary": getattr(entry, "summary", ""),
            "image": None,
        }
        articles.append(article)
    return articles
