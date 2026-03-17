from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modules.topic_processing import TopicProcessor
from utils.config import TFIDF_SIMILARITY_THRESHOLD, RISING_SCORE_DEFAULT


def aggregate_topics(all_raw_data, category_name, seeds):
    """Aggregate topics from multiple seed keyword results (Top + Rising).
    Applies domain-keyword relevance filtering per category.
    """
    aggregated = defaultdict(lambda: {
        "scores": [],
        "sources": set(),
        "is_rising": False,
    })

    for item in all_raw_data:
        keyword = item["keyword"]
        related = item["data"].get("related_topics", {})

        for t in related.get("top", []):
            raw_name = t["topic"]["title"]
            try:
                score = int(t["value"])
            except (ValueError, TypeError):
                continue
            clean_name = TopicProcessor.clean(raw_name)
            if clean_name and TopicProcessor.is_relevant(clean_name, category_name):
                final_name = TopicProcessor.normalize(clean_name)
                aggregated[final_name]["scores"].append(score)
                aggregated[final_name]["sources"].add(keyword)

        for t in related.get("rising", []):
            raw_name = t["topic"]["title"]
            clean_name = TopicProcessor.clean(raw_name)
            if clean_name and TopicProcessor.is_relevant(clean_name, category_name):
                final_name = TopicProcessor.normalize(clean_name)
                aggregated[final_name]["is_rising"] = True
                if not aggregated[final_name]["scores"]:
                    aggregated[final_name]["scores"].append(RISING_SCORE_DEFAULT)

    aggregated = _tfidf_filter(aggregated, seeds)

    return aggregated


def _tfidf_filter(aggregated, seeds):
    """Remove topics whose TF-IDF cosine similarity to all seed keywords
    falls below the configured threshold."""
    topic_names = list(aggregated.keys())
    if len(topic_names) < 2:
        return aggregated

    corpus = seeds + topic_names
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    seed_vectors = tfidf_matrix[: len(seeds)]
    topic_vectors = tfidf_matrix[len(seeds):]

    sim_matrix = cosine_similarity(topic_vectors, seed_vectors)

    filtered = {}
    for idx, name in enumerate(topic_names):
        max_sim = sim_matrix[idx].max()
        if max_sim >= TFIDF_SIMILARITY_THRESHOLD:
            filtered[name] = aggregated[name]

    return filtered


def calculate_final_scores(aggregated, news_data=None):
    """Calculate final score, star rating, and explanation for each topic."""
    results = []

    for topic, data in aggregated.items():
        scores = data["scores"]
        if not scores:
            continue
        occurrence = len(scores)
        avg_score = sum(scores) / occurrence

        occurrence_weight = min(1 + (occurrence - 1) * 0.15, 2.0)
        final_score = min(round(avg_score * occurrence_weight), 100)

        news_count = 0
        if news_data and topic in news_data:
            news_count = news_data[topic]
            final_score = min(round(final_score + min(news_count * 0.5, 10)), 100)

        stars = _score_to_stars(final_score)
        reason = _generate_explanation(
            final_score, occurrence, data["is_rising"], news_count,
        )

        results.append({
            "topic": topic,
            "avg_score": round(avg_score, 1),
            "occurrence": occurrence,
            "final_score": final_score,
            "stars": stars,
            "reason": reason,
            "is_rising": data["is_rising"],
        })

    results.sort(key=lambda x: x["final_score"], reverse=True)

    for i, r in enumerate(results, 1):
        r["rank"] = i

    return results


def _score_to_stars(score):
    if score >= 80:
        return 5
    if score >= 60:
        return 4
    if score >= 40:
        return 3
    if score >= 20:
        return 2
    return 1


def _generate_explanation(score, occurrence, is_rising, news_count):
    if score >= 80 and occurrence >= 3:
        base = "Dominant trend with broad search interest"
    elif score >= 80:
        base = "Rapid increase in search interest"
    elif score >= 50 and occurrence >= 3:
        base = "Consistently trending across related topics"
    elif is_rising:
        base = "Emerging trend gaining momentum"
    elif score >= 50:
        base = "Moderate and steady search interest"
    else:
        base = "Increasing public interest"

    if news_count >= 5:
        base += " with strong news coverage"
    elif news_count >= 1:
        base += " with some news coverage"

    return base
