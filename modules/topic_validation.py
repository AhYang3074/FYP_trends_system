import requests
from utils.config import (
    NEWS_API_KEY,
    GNEWS_API_KEY,
    ALPHA_VANTAGE_KEY,
    STACKEXCHANGE_KEY,
    VALIDATION_SOURCES,
    VALIDATION_MAX_BONUS,
    VALIDATION_TOTAL_CAP,
)

_TIMEOUT = 5


def validate_topics(topic_names, category_name):
    cat = category_name.lower()
    sources = VALIDATION_SOURCES.get(cat, ["news"])

    dispatcher = {
        "news":          _news_validate,
        "alphavantage":  _alphavantage_validate,
        "github":        _github_validate,
        "stackexchange": _stackexchange_validate,
    }

    raw = {topic: {} for topic in topic_names}

    for src in sources:
        fn = dispatcher.get(src)
        if fn is None:
            continue
        src_results = fn(topic_names)
        for topic in topic_names:
            raw[topic][src] = src_results.get(topic, 0)

    result = {}
    for topic in topic_names:
        total_bonus = 0.0
        for src, raw_val in raw[topic].items():
            max_b = VALIDATION_MAX_BONUS.get(src, 5)
            total_bonus += _normalise(raw_val, src, max_b)
        total_bonus = min(total_bonus, VALIDATION_TOTAL_CAP)
        result[topic] = {
            "bonus": round(total_bonus, 2),
            "sources": raw[topic],
        }

    return result


def _normalise(raw_value, source, max_bonus):
    if raw_value <= 0:
        return 0.0
    thresholds = {
        "news":          50,
        "alphavantage":  10,
        "github":        5000,
        "stackexchange": 200,
    }
    ceiling = thresholds.get(source, 50)
    return min(raw_value / ceiling, 1.0) * max_bonus


def _news_validate(topics):
    newsapi_data = _newsapi_fetch(topics)
    gnews_data = _gnews_fetch(topics)

    out = {}
    for topic in topics:
        na = newsapi_data.get(topic, 0)
        gn = gnews_data.get(topic, 0)
        out[topic] = round(na * 0.6 + gn * 0.4)
    return out


def _newsapi_fetch(topics):
    if not NEWS_API_KEY:
        return {}
    out = {}
    for topic in topics:
        try:
            resp = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": topic,
                    "sortBy": "relevancy",
                    "pageSize": 5,
                    "apiKey": NEWS_API_KEY,
                },
                timeout=_TIMEOUT,
            )
            if resp.status_code == 200:
                out[topic] = resp.json().get("totalResults", 0)
        except Exception:
            pass
    return out


def _gnews_fetch(topics):
    if not GNEWS_API_KEY:
        return {}
    out = {}
    for topic in topics:
        try:
            resp = requests.get(
                "https://gnews.io/api/v4/search",
                params={
                    "q": topic,
                    "lang": "en",
                    "max": 5,
                    "apikey": GNEWS_API_KEY,
                },
                timeout=_TIMEOUT,
            )
            if resp.status_code == 200:
                out[topic] = resp.json().get("totalArticles", 0)
        except Exception:
            pass
    return out


def _alphavantage_validate(topics):
    if not ALPHA_VANTAGE_KEY:
        return {}
    out = {}
    for topic in topics:
        try:
            resp = requests.get(
                "https://www.alphavantage.co/query",
                params={
                    "function": "NEWS_SENTIMENT",
                    "topics": topic,
                    "limit": 10,
                    "apikey": ALPHA_VANTAGE_KEY,
                },
                timeout=_TIMEOUT,
            )
            if resp.status_code == 200:
                out[topic] = len(resp.json().get("feed", []))
        except Exception:
            pass
    return out


def _github_validate(topics):
    out = {}
    for topic in topics:
        try:
            resp = requests.get(
                "https://api.github.com/search/repositories",
                params={
                    "q": topic,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 5,
                },
                headers={"Accept": "application/vnd.github.v3+json"},
                timeout=_TIMEOUT,
            )
            if resp.status_code == 200:
                stars = sum(
                    r["stargazers_count"]
                    for r in resp.json().get("items", [])
                )
                out[topic] = stars
        except Exception:
            pass
    return out


def _stackexchange_validate(topics):
    if not STACKEXCHANGE_KEY:
        return {}
    out = {}
    for topic in topics:
        try:
            resp = requests.get(
                "https://api.stackexchange.com/2.3/search",
                params={
                    "order": "desc",
                    "sort": "relevance",
                    "intitle": topic,
                    "site": "stackoverflow",
                    "pagesize": 1,
                    "filter": "total",
                    "key": STACKEXCHANGE_KEY,
                },
                timeout=_TIMEOUT,
            )
            if resp.status_code == 200:
                out[topic] = resp.json().get("total", 0)
        except Exception:
            pass
    return out
