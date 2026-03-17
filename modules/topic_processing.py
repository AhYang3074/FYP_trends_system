from utils.config import DOMAIN_KEYWORDS, DOMAIN_EXCLUSIONS, TOPIC_SUBCATEGORIES


class TopicProcessor:
    # L1 — single-word noise (exact match, pre-normalize)
    GENERIC_WORDS = {
        "news", "price", "data", "review", "update", "latest",
        "best", "top", "free", "online", "download", "app",
        "website", "tool", "service", "company", "stock",
        "video", "photo", "image", "map", "list", "guide",
        "today", "near me", "login", "sign up",
    }

    REPLACEMENTS = {
        # Abbreviation → full form
        "ai": "artificial intelligence",
        "a.i.": "artificial intelligence",
        "artificial intelligence (ai)": "artificial intelligence",
        "ml": "machine learning",
        "dl": "deep learning",
        "deep learning (dl)": "deep learning",
        "nlp": "natural language processing",
        "iot": "internet of things",
        "vr": "virtual reality",
        "ar": "augmented reality",
        "ev": "electric vehicle",
        "cs": "computer science",
        "se": "software engineering",
        "ds": "data science",
        "os": "operating system",
        # Standalone fragments → full concept (exact match only)
        "intelligence": "artificial intelligence",
        "machine": "machine learning",
        "learning": "machine learning",
        "cyber": "cybersecurity",
        "blockchain": "blockchain technology",
        "cloud": "cloud computing",
    }

    # L1.5 — too-broad standalone topics (exact match, post-normalize)
    GENERIC_TOPICS = {
        "technology", "software", "internet", "science",
        "data", "system", "platform", "application",
        "network", "computer", "engineering", "computing",
        "information", "digital", "security", "analysis",
        "management", "research", "development", "design",
        "process", "model", "program", "solution",
    }

    # L1.5 — temporal / seasonal noise (substring match)
    TEMPORAL_NOISE = [
        "summer", "winter", "spring", "fall",
        "autumn", "holiday", "festival", "event",
        "christmas", "halloween", "new year",
        "black friday", "cyber monday", "valentine",
    ]

    # --- Layer 1: Basic Cleaning ---
    @staticmethod
    def clean(name):
        """Filter out very short or generic single words."""
        name = name.lower().strip()
        if not name or len(name) < 2:
            return None
        if name in TopicProcessor.GENERIC_WORDS:
            return None
        return name

    @staticmethod
    def normalize(name):
        return TopicProcessor.REPLACEMENTS.get(name, name)

    # --- Layer 1.5: Generic / temporal filter (runs on normalized name) ---
    @staticmethod
    def is_noise(name):
        """Catch overly broad topics and seasonal words.
        Runs AFTER normalize() so 'machine' → 'machine learning' survives."""
        if name in TopicProcessor.GENERIC_TOPICS:
            return True
        if any(t in name for t in TopicProcessor.TEMPORAL_NOISE):
            return True
        return False

    # --- Layer 2: Keyword match score (continuous) ---
    @staticmethod
    def keyword_match_score(name, category_name):
        """Return 1.0 (core match), 0.8 (related match), or 0.0 (no match)."""
        domain = DOMAIN_KEYWORDS.get(category_name.lower())
        if not domain:
            return 1.0
        if any(k in name for k in domain["core"]):
            return 1.0
        if any(k in name for k in domain["related"]):
            return 0.8
        return 0.0

    # --- Layer 3: Exclusion (hard delete) ---
    @staticmethod
    def is_excluded(name, category_name):
        exclusions = DOMAIN_EXCLUSIONS.get(category_name.lower(), [])
        return any(ex in name for ex in exclusions)

    # --- Sub-category inference ---
    @staticmethod
    def infer_subcategory(name, category_name):
        """Match topic against TOPIC_SUBCATEGORIES patterns.
        Returns the first matching sub-category or 'General'."""
        subcats = TOPIC_SUBCATEGORIES.get(category_name.lower(), {})
        for subcat, patterns in subcats.items():
            if any(p in name for p in patterns):
                return subcat
        return "General"
