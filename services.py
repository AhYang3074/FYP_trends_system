from serpapi import GoogleSearch

API_KEY = "369f0b4b9ce8b12731be53573f456cb9b2653cfa5eaa0d8eea9cd7ecd7f650cc"

def fetch_trends_data(keyword):
    params = {
        "engine": "google_trends",
        "q": keyword,
        "data_type": "RELATED_TOPICS",
        "api_key": API_KEY
    }
    search = GoogleSearch(params)
    return search.get_dict()