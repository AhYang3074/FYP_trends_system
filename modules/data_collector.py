from serpapi import GoogleSearch
from utils.config import SERPAPI_KEY, DEFAULT_CATEGORY, DEFAULT_DATE_RANGE


def fetch_related_topics(keyword, category=DEFAULT_CATEGORY, date=DEFAULT_DATE_RANGE):
    """Fetch related topics (Top + Rising) for a single keyword."""
    params = {
        "engine": "google_trends",
        "q": keyword,
        "cat": category,
        "date": date,
        "data_type": "RELATED_TOPICS",
        "api_key": SERPAPI_KEY,
    }
    search = GoogleSearch(params)
    return search.get_dict()


def fetch_multi_seed(keywords, category=DEFAULT_CATEGORY, date=DEFAULT_DATE_RANGE):
    """Fetch related topics for multiple seed keywords and return all results."""
    all_results = []
    for kw in keywords:
        kw = kw.strip()
        if not kw:
            continue
        try:
            data = fetch_related_topics(kw, category, date)
            all_results.append({"keyword": kw, "data": data})
        except Exception:
            continue
    return all_results
