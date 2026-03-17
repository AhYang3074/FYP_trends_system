from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modules.topic_processing import TopicProcessor
from utils.config import (
    DOMAIN_KEYWORDS,
    TFIDF_SIMILARITY_THRESHOLD,
    RISING_SCORE_DEFAULT,
    RELEVANCE_FLOOR,
    ENTITY_PENALTY,
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
        "is_entity": False,
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
    """Run L1 → L3, then store the topic. Returns the entry or None."""
    clean_name = TopicProcessor.clean(raw_name)
    if not clean_name:
        return None
    final_name = TopicProcessor.normalize(clean_name)
    if TopicProcessor.is_excluded(final_name, category_name):
        return None

    entry = aggregated[final_name]

    kw_score = TopicProcessor.keyword_match_score(final_name, category_name)
    entry["keyword_score"] = max(entry["keyword_score"], kw_score)

    if TopicProcessor.is_entity(final_name):
        entry["is_entity"] = True

    if score is not None:
        entry["scores"].append(score)
        entry["sources"].add(seed_keyword)

    return entry


# ── L4: TF-IDF against full domain vocabulary ──────────────────────────────
def _attach_tfidf_scores(aggregated, category_name, seeds):
    """Cosine similarity of each topic to every core + related keyword + seed.
    Uses the full domain vocabulary so semantic neighbours are caught even
    when they don't appear in the keyword lists."""
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
def _compute_relevance(keyword_score, tfidf_sim, is_entity):
    """Combine keyword match + TF-IDF into a single 0‥1 relevance multiplier.
    Core match   → 1.0
    Related match → 0.85
    No keyword match → scaled TF-IDF (capped at 0.7, floor at RELEVANCE_FLOOR)
    Entity → heavy penalty on top.
    """
    if keyword_score >= 1.0:
        rel = 1.0
    elif keyword_score >= 0.8:
        rel = 0.85
    else:
        rel = min(tfidf_sim * 1.5, 0.7)
        rel = max(rel, RELEVANCE_FLOOR)

    if is_entity:
        rel *= ENTITY_PENALTY

    return rel


# ── Final scoring ───────────────────────────────────────────────────────────
def calculate_final_scores(aggregated, news_data=None):
    results = []

    for topic, data in aggregated.items():
        scores = data["scores"]
        if not scores:
            continue

        occurrence = len(scores)
        avg_score = sum(scores) / occurrence

        # Multi-seed occurrence boost (stronger reward for cross-seed presence)
        occurrence_weight = min(1 + (occurrence - 1) * 0.25, 2.5)

        # Continuous relevance multiplier (keyword + TF-IDF + entity)
        relevance = _compute_relevance(
            data["keyword_score"],
            data.get("tfidf_sim", 0.0),
            data["is_entity"],
        )

        final_score = avg_score * occurrence_weight * relevance

        # News bonus
        news_count = 0
        if news_data and topic in news_data:
            news_count = news_data[topic]
            final_score += min(news_count * 0.5, 10)

        final_score = max(min(round(final_score), 100), 1)

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
