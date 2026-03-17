from utils.config import DOMAIN_KEYWORDS, DOMAIN_EXCLUSIONS, ENTITY_INDICATORS


class TopicProcessor:
    GENERIC_WORDS = {
        "news", "price", "data", "review", "update", "latest",
        "best", "top", "free", "online", "download", "app",
        "website", "tool", "service", "company", "stock",
    }

    REPLACEMENTS = {
        "ai": "artificial intelligence",
        "artificial intelligence (ai)": "artificial intelligence",
        "a.i.": "artificial intelligence",
        "ml": "machine learning",
        "deep learning (dl)": "deep learning",
        "dl": "deep learning",
        "nlp": "natural language processing",
        "iot": "internet of things",
        "vr": "virtual reality",
        "ar": "augmented reality",
        "ev": "electric vehicle",
        "saas": "software as a service",
    }

    # --- Layer 1: Basic Cleaning ---
    @staticmethod
    def clean(name):
        """Filter out single-word or generic topics."""
        name = name.lower().strip()
        if len(name.split()) < 2:
            return None
        if name in TopicProcessor.GENERIC_WORDS:
            return None
        return name

    @staticmethod
    def normalize(name):
        return TopicProcessor.REPLACEMENTS.get(name, name)

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

    # --- Entity detection ---
    @staticmethod
    def is_entity(name):
        """Detect geographic, institutional, or reference-site entities."""
        return any(ind in name for ind in ENTITY_INDICATORS)
