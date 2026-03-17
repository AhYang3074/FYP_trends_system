from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def cluster_topics(topic_names, n_clusters=None):
    """Cluster topics using TF-IDF vectorization + K-Means."""
    if len(topic_names) < 3:
        return {name: 0 for name in topic_names}

    if n_clusters is None:
        n_clusters = min(max(2, len(topic_names) // 3), 5)
    n_clusters = min(n_clusters, len(topic_names))

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(topic_names)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(tfidf_matrix)

    return {name: int(label) for name, label in zip(topic_names, labels)}
