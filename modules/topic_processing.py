from utils.config import DOMAIN_KEYWORDS, DOMAIN_EXCLUSIONS


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

    @staticmethod
    def clean(name):
        """Filter out single-word or generic topics."""
        name = name.lower().strip()
        tokens = name.split()
        if len(tokens) < 2:
            return None
        if name in TopicProcessor.GENERIC_WORDS:
            return None
        return name

    @staticmethod
    def normalize(name):
        """Map abbreviations/synonyms to a canonical form."""
        return TopicProcessor.REPLACEMENTS.get(name, name)

    @staticmethod
    def is_relevant(name, category_name):
        """Two-stage relevance check:
        1. Reject if topic contains any exclusion term.
        2. Accept only if topic contains at least one domain keyword.
        """
        cat = category_name.lower()

        exclusions = DOMAIN_EXCLUSIONS.get(cat, [])
        if any(ex in name for ex in exclusions):
            return False

        keywords = DOMAIN_KEYWORDS.get(cat, [])
        if not keywords:
            return True
        return any(kw in name for kw in keywords)
