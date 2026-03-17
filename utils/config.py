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

# Compound phrases preferred over single generic words to avoid false positives
DOMAIN_KEYWORDS = {
    "technology": [
        "artificial intelligence", "machine learning", "deep learning",
        "cyber", "security", "cloud computing", "blockchain", "software",
        "computing", "tech", "digital", "algorithm", "robot", "automat",
        "neural", "network", "quantum", "program", "code", "hardware",
        "chip", "semiconductor", "gpu", "api", "platform", "saas",
        "devops", "web", "internet", "database", "server", "encryption",
        "malware", "phishing", "firewall", "virtuali", "container",
        "microservice", "llm", "chatbot", "generative", "data science",
        "open source", "cryptograph",
    ],
    "finance": [
        "stock market", "invest", "trading", "banking", "finance",
        "cryptocurren", "fund", "portfolio", "dividend", "bond",
        "interest rate", "forex", "wealth", "capital", "asset", "fintech",
        "payment", "insurance", "credit", "loan", "mortgage", "economy",
        "inflation", "fiscal", "revenue", "equity", "hedge", "commodity",
        "valuation", "ipo", "wall street",
    ],
    "business": [
        "startup", "entrepreneur", "e-commerce", "ecommerce", "commerce",
        "marketing", "supply chain", "brand", "management", "retail",
        "strategy", "leadership", "innovation", "merger", "acquisition",
        "franchise", "revenue", "profit", "corporate", "logistics",
        "consult", "outsourc", "b2b", "b2c", "saas", "crm",
        "business model", "venture", "partnership", "stakeholder",
        "workforce", "hiring", "recruitment", "competitive",
    ],
    "health": [
        "health", "medical", "doctor", "patient", "hospital", "disease",
        "therapy", "mental", "wellness", "nutrition", "diet", "fitness",
        "pharma", "vaccine", "clinic", "diagnos", "treatment", "medicine",
        "symptom", "biotech", "genome", "cancer", "virus", "surgery",
        "cardio", "immun", "epidem", "chronic", "drug", "supplement",
    ],
    "science": [
        "space", "climate", "quantum", "physics", "biology", "chemistry",
        "energy", "renewable", "solar", "nuclear", "genome", "research",
        "experiment", "planet", "nasa", "satellite", "carbon", "emission",
        "evolution", "ecosystem", "telescope", "particle", "molecule",
        "fossil", "biodiversity", "astro", "neurosci", "geolog",
    ],
    "all categories": [],
}

# Topics containing any exclusion term are rejected regardless of keyword match
DOMAIN_EXCLUSIONS = {
    "technology": [
        "county", "zodiac", "university", "college", "country",
        "religion", "church", "football", "basketball", "soccer",
        "recipe", "cooking", "fashion", "celebrity", "movie",
    ],
    "finance": [
        "recipe", "cooking", "football", "basketball", "soccer",
        "movie", "celebrity", "fashion", "power supply", "circuit",
    ],
    "business": [
        "power supply", "voltage", "watt", "circuit", "electric",
        "recipe", "cooking", "football", "basketball", "soccer",
        "movie", "celebrity", "county", "zodiac", "university",
        "college", "religion", "church", "fashion",
    ],
    "health": [
        "football", "soccer", "celebrity", "fashion", "movie",
        "county", "zodiac", "power supply", "circuit", "voltage",
    ],
    "science": [
        "football", "soccer", "celebrity", "fashion", "movie",
        "county", "zodiac", "recipe", "cooking",
    ],
    "all categories": [],
}

TFIDF_SIMILARITY_THRESHOLD = 0.12
RISING_SCORE_DEFAULT = 15
