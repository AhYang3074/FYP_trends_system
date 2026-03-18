from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modules.topic_processing import TopicProcessor
from utils.config import (
    DOMAIN_KEYWORDS,
    TFIDF_SIMILARITY_THRESHOLD,
    RISING_SCORE_DEFAULT,
    RELEVANCE_FLOOR,
)


# ── Pipeline ────────────────────────────────────────────────────────────────
def aggregate_topics(all_raw_data, category_name, seeds):
    """Collect and tag every topic. Only L1 (clean) and L3 (exclusion) delete.
    Everything else becomes a continuous score modifier."""
    aggregated = defaultdict(lambda: {
        "scores": [],
        "sources": set(),
        "is_rising": False,
        "keyword_score": 0.0,
        "subcategory": "General",
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
            _ingest(aggregated, raw_name, score, keyword, category_name)

        for t in related.get("rising", []):
            raw_name = t["topic"]["title"]
            entry = _ingest(aggregated, raw_name, None, keyword, category_name)
            if entry is not None:
                entry["is_rising"] = True
                if not entry["scores"]:
                    entry["scores"].append(RISING_SCORE_DEFAULT)

    _attach_tfidf_scores(aggregated, category_name, seeds)

    return aggregated


def _ingest(aggregated, raw_name, score, seed_keyword, category_name):
    """Run L1 → L1.5 → L3, then store the topic. Returns the entry or None."""
    clean_name = TopicProcessor.clean(raw_name)
    if not clean_name:
        return None
    final_name = TopicProcessor.normalize(clean_name)
    if TopicProcessor.is_noise(final_name):
        return None
    if TopicProcessor.is_excluded(final_name, category_name):
        return None

    entry = aggregated[final_name]

    kw_score = TopicProcessor.keyword_match_score(final_name, category_name)
    entry["keyword_score"] = max(entry["keyword_score"], kw_score)

    subcat = TopicProcessor.infer_subcategory(final_name, category_name)
    if entry["subcategory"] == "General" and subcat != "General":
        entry["subcategory"] = subcat

    if score is not None:
        entry["scores"].append(score)
        entry["sources"].add(seed_keyword)

    return entry


# ── L4: TF-IDF against full domain vocabulary ──────────────────────────────
def _attach_tfidf_scores(aggregated, category_name, seeds):
    topic_names = list(aggregated.keys())
    if not topic_names:
        return

    domain = DOMAIN_KEYWORDS.get(category_name.lower(), {"core": [], "related": []})
    reference_docs = list(dict.fromkeys(
        domain["core"] + domain["related"] + seeds
    ))

    if not reference_docs:
        for name in topic_names:
            aggregated[name]["tfidf_sim"] = 1.0
        return

    corpus = reference_docs + topic_names
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    ref_vectors = tfidf_matrix[: len(reference_docs)]
    topic_vectors = tfidf_matrix[len(reference_docs) :]

    sim_matrix = cosine_similarity(topic_vectors, ref_vectors)

    for idx, name in enumerate(topic_names):
        aggregated[name]["tfidf_sim"] = float(sim_matrix[idx].max())


# ── Relevance formula ───────────────────────────────────────────────────────
def _compute_relevance(keyword_score, tfidf_sim):
    if keyword_score >= 1.0:
        return 1.0
    if keyword_score >= 0.8:
        return 0.85

    if tfidf_sim >= TFIDF_SIMILARITY_THRESHOLD:
        return min(tfidf_sim * 1.5, 0.7)
    return RELEVANCE_FLOOR


# ── Final scoring ───────────────────────────────────────────────────────────
def calculate_final_scores(aggregated, validation_data=None):
    results = []

    for topic, data in aggregated.items():
        scores = data["scores"]
        if not scores:
            continue

        occurrence = len(scores)
        avg_score = sum(scores) / occurrence

        occurrence_weight = min(1 + (occurrence - 1) * 0.25, 2.5)

        relevance = _compute_relevance(
            data["keyword_score"],
            data.get("tfidf_sim", 0.0),
        )

        final_score = avg_score * occurrence_weight * relevance

        trend_bonus = TopicProcessor.trend_boost(topic)
        final_score += trend_bonus

        validation_bonus = 0.0
        validation_sources = {}
        if validation_data and topic in validation_data:
            vd = validation_data[topic]
            validation_bonus = vd.get("bonus", 0.0)
            validation_sources = vd.get("sources", {})
            final_score += validation_bonus

        final_score = max(min(round(final_score), 100), 1)

        stars = _score_to_stars(final_score)
        reason = _generate_explanation(
            final_score, occurrence, data["is_rising"],
            validation_bonus, validation_sources,
        )

        results.append({
            "topic": TopicProcessor.display_name(topic),
            "subcategory": data["subcategory"],
            "avg_score": round(avg_score, 1),
            "occurrence": occurrence,
            "final_score": final_score,
            "stars": stars,
            "reason": reason,
            "is_rising": data["is_rising"],
            "validation": validation_sources,
        })

    results.sort(key=lambda x: x["final_score"], reverse=True)

    for i, r in enumerate(results, 1):
        r["rank"] = i

    return results


# ── Helpers ─────────────────────────────────────────────────────────────────
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


def _generate_explanation(score, occurrence, is_rising, bonus, sources):
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

    signals = []
    if sources.get("news", 0) > 0:
        signals.append("news coverage")
    if sources.get("github", 0) > 0:
        signals.append("GitHub")
    if sources.get("stackexchange", 0) > 0:
        signals.append("StackOverflow")
    if sources.get("alphavantage", 0) > 0:
        signals.append("financial media")

    if signals:
        base += " — validated by " + ", ".join(signals)

    return base
