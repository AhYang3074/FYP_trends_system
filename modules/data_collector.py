from serpapi import GoogleSearch
from utils.config import SERPAPI_KEY, DEFAULT_CATEGORY, DEFAULT_DATE_RANGE


def fetch_related_topics(keyword, category=DEFAULT_CATEGORY, date=DEFAULT_DATE_RANGE):
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
    """One request per seed; `date` is the full window (e.g. today 12-m or today 1-m)."""
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
