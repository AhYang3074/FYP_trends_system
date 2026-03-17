class TopicProcessor:
    GENERIC_WORDS = {"news", "price", "data", "review"}
    REPLACEMENTS = {
        "ai": "artificial intelligence",
        "artificial intelligence (ai)": "artificial intelligence",
        "ml": "machine learning",
    }

    @staticmethod
    def clean(name):
        name = name.lower().strip()
        if len(name.split()) < 2 or name in TopicProcessor.GENERIC_WORDS:
            return None
        return name

    @staticmethod
    def normalize(name):
        return TopicProcessor.REPLACEMENTS.get(name, name)
