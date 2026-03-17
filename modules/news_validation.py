import requests
from utils.config import NEWS_API_KEY


def validate_topics(topic_names):
    """Check each topic against NewsAPI. Returns {topic: article_count}.
    Gracefully returns empty dict if NEWS_API_KEY is not configured.
    """
    if not NEWS_API_KEY:
        return {}

    news_data = {}
    for topic in topic_names:
        try:
            resp = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": topic,
                    "sortBy": "relevancy",
                    "pageSize": 5,
                    "apiKey": NEWS_API_KEY,
                },
                timeout=5,
            )
            if resp.status_code == 200:
                news_data[topic] = resp.json().get("totalResults", 0)
        except Exception:
            continue
    return news_data
