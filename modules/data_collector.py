from serpapi import GoogleSearch
from utils.config import SERPAPI_KEY, DEFAULT_CATEGORY, DEFAULT_DATE_RANGE


def fetch_trends_data(keyword, category=DEFAULT_CATEGORY, date=DEFAULT_DATE_RANGE):
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
