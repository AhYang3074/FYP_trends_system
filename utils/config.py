import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

DEFAULT_CATEGORY = "18"
DEFAULT_DATE_RANGE = "today 1-m"

CATEGORY_SEEDS = {
    "0": {
        "name": "All Categories",
        "seeds": [
            "trending", "viral", "popular", "breaking news", "top stories",
        ],
    },
    "18": {
        "name": "Technology",
        "seeds": [
            "artificial intelligence", "machine learning", "cybersecurity",
            "blockchain", "cloud computing",
        ],
    },
    "7": {
        "name": "Finance",
        "seeds": [
            "stock market", "cryptocurrency", "investment",
            "banking", "fintech",
        ],
    },
    "3": {
        "name": "Business",
        "seeds": [
            "startup", "entrepreneurship", "e-commerce",
            "marketing", "supply chain",
        ],
    },
    "13": {
        "name": "Health",
        "seeds": [
            "mental health", "nutrition", "fitness",
            "medical research", "public health",
        ],
    },
    "174": {
        "name": "Science",
        "seeds": [
            "space exploration", "climate change", "quantum physics",
            "biotechnology", "renewable energy",
        ],
    },
}

# ---------------------------------------------------------------------------
# Layer 2: Domain keyword matching  (core → 1.0, related → 0.8, miss → 0.0)
# ---------------------------------------------------------------------------
DOMAIN_KEYWORDS = {
    "technology": {
        "core": [
            "artificial intelligence", "machine learning", "deep learning",
            "cybersecurity", "cloud computing", "blockchain",
        ],
        "related": [
            "software", "hardware", "algorithm", "automation",
            "neural", "network", "chatbot", "api",
            "database", "server", "programming", "code", "developer",
            "web", "internet", "platform", "saas", "devops",
            "gpu", "chip", "semiconductor", "encryption", "malware",
            "firewall", "virtuali", "container", "microservice",
            "generative", "open source", "crypto", "robot",
            "digital", "cyber", "tech", "computing", "quantum",
            "llm", "data science", "computer security",
        ],
    },
    "finance": {
        "core": [
            "stock market", "investment", "trading",
            "cryptocurrency", "interest rate",
        ],
        "related": [
            "banking", "finance", "portfolio", "asset",
            "equity", "bond", "fund", "wealth",
            "forex", "inflation", "economy", "fintech",
            "dividend", "mortgage", "loan", "credit",
            "fiscal", "hedge", "commodity", "valuation",
            "ipo", "wall street", "payment", "insurance",
        ],
    },
    "business": {
        "core": [
            "startup", "entrepreneurship", "business strategy",
            "supply chain", "marketing strategy",
        ],
        "related": [
            "management", "brand", "commerce", "ecommerce",
            "retail", "logistics", "operation", "corporate",
            "revenue", "profit", "growth", "venture",
            "investment", "customer", "market",
            "franchise", "merger", "acquisition", "stakeholder",
            "workforce", "hiring", "recruitment", "competitive",
            "outsourc", "consult", "b2b", "b2c", "crm",
            "partnership", "innovation", "strategy", "leadership",
        ],
    },
    "health": {
        "core": [
            "mental health", "public health", "medical research",
            "disease treatment",
        ],
        "related": [
            "fitness", "nutrition", "wellness",
            "hospital", "doctor", "patient",
            "therapy", "medicine", "vaccine",
            "pharma", "clinic", "diagnos", "treatment",
            "symptom", "biotech", "genome", "cancer",
            "virus", "surgery", "cardio", "immun",
            "epidem", "chronic", "drug", "supplement",
            "health", "medical", "diet",
        ],
    },
    "science": {
        "core": [
            "quantum physics", "climate change",
            "space exploration", "biotechnology",
        ],
        "related": [
            "research", "experiment", "energy",
            "solar", "nuclear", "genome",
            "biology", "chemistry", "physics",
            "renewable", "satellite", "carbon", "emission",
            "evolution", "ecosystem", "telescope", "particle",
            "molecule", "fossil", "biodiversity", "astro",
            "neurosci", "geolog", "planet", "nasa",
        ],
    },
    "all categories": {"core": [], "related": []},
}

# ---------------------------------------------------------------------------
# Layer 3: Hard exclusions — instant delete
# ---------------------------------------------------------------------------
DOMAIN_EXCLUSIONS = {
    "technology": [
        "county", "zodiac", "university", "college", "country",
        "religion", "church", "football", "basketball", "soccer",
        "recipe", "cooking", "fashion", "celebrity", "movie",
        "power supply", "real estate", "weight loss",
        "prom dress", "white gold", "gold price",
    ],
    "finance": [
        "recipe", "cooking", "football", "basketball", "soccer",
        "movie", "celebrity", "fashion", "power supply", "circuit",
        "voltage", "university", "college", "zodiac",
        "prom dress", "white gold",
    ],
    "business": [
        "power supply", "voltage", "watt", "circuit", "electric",
        "recipe", "cooking", "football", "basketball", "soccer",
        "movie", "celebrity", "county", "zodiac", "university",
        "college", "religion", "church", "fashion", "weight loss",
        "real estate agent", "prom dress", "white gold",
    ],
    "health": [
        "football", "soccer", "celebrity", "fashion", "movie",
        "county", "zodiac", "power supply", "circuit", "voltage",
        "stock market", "cryptocurrency",
    ],
    "science": [
        "football", "soccer", "celebrity", "fashion", "movie",
        "county", "zodiac", "recipe", "cooking",
        "stock market", "cryptocurrency",
    ],
    "all categories": [],
}

# ---------------------------------------------------------------------------
# Entity indicators — geographic / institutional / reference-site noise
# ---------------------------------------------------------------------------
ENTITY_INDICATORS = [
    "united states", "united kingdom", "south korea", "north korea",
    "saudi arabia", "new zealand", "hong kong", "sri lanka",
    "costa rica", "puerto rico", "el salvador", "dominican republic",
    "czech republic", "ivory coast",
    "province", "prefecture", "district",
    "wiki", "brilliant math", "imdb",
]

# ---------------------------------------------------------------------------
# Scoring parameters
# ---------------------------------------------------------------------------
TFIDF_SIMILARITY_THRESHOLD = 0.05
RELEVANCE_FLOOR = 0.15
ENTITY_PENALTY = 0.1

RISING_SCORE_DEFAULT = 15
