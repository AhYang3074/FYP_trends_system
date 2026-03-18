import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", "")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY", "")
STACKEXCHANGE_KEY = os.getenv("STACKEXCHANGE_KEY", "")

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
            "large language model", "generative ai", "artificial intelligence",
            "machine learning", "cybersecurity", "blockchain", "cloud computing",
            "chatgpt", "openai", "gpt", "gemini", "copilot", "claude",
            "data science", "software engineering", "internet technology",
            "neural", "transformer", "ai agent", "ai model",
            "ai regulation", "ai safety", "chatbot",
            "natural language", "computer vision", "deepseek",
        ],
    },
    "7": {
        "name": "Finance",
        "seeds": [
            "inflation", "interest rate", "federal reserve", "central bank",
            "recession", "gdp", "monetary policy",
            "unemployment rate", "consumer price index",
            "cpi inflation", "interest rate hike",
            "fed rate decision", "economic outlook",
            "stock market", "nasdaq", "s&p 500", "dow jones",
            "equity trading", "ipo", "earnings report",
            "stock earnings", "quarterly earnings",
            "stock rally", "market crash", "bull market", "bear market",
            "stock valuation",
            "bitcoin", "ethereum", "crypto market", "defi",
            "stablecoin", "crypto regulation",
            "crypto trading", "crypto exchange", "crypto crash",
            "web3 finance",
            "digital payment", "fintech", "neobank",
            "payment gateway", "mobile banking",
            "digital wallet", "mobile payment",
            "contactless payment", "buy now pay later",
            "hedge fund", "etf", "derivatives", "forex trading",
            "asset management", "portfolio management",
            "risk management", "capital market", "private equity",
        ],
    },
    "3": {
        "name": "Business",
        "seeds": [
            "startup funding", "venture capital", "series a funding",
            "unicorn startup", "pitch deck", "business innovation",
            "business strategy", "corporate strategy", "leadership",
            "organizational management", "ai marketing strategy",
            "digital marketing", "seo", "content marketing",
            "social media marketing", "branding", "marketing strategy",
            "ecommerce", "online business", "shopify", "amazon seller",
            "dropshipping",
            "supply chain", "logistics", "inventory management",
            "creator economy", "gig economy", "remote work",
            "digital transformation",
        ],
    },
    "13": {
        "name": "Health",
        "seeds": [
            "public health", "healthcare system", "hospital management",
            "chronic disease", "cancer research", "diabetes treatment",
            "heart disease",
            "biotechnology", "genome sequencing", "gene therapy", "crispr",
            "vaccine development", "clinical trial", "pharmaceutical industry",
            "mental health", "depression", "anxiety",
            "telemedicine", "digital health", "wearable health",
            "health technology",
        ],
    },
    "174": {
        "name": "Science",
        "seeds": [
            "space exploration", "mars mission", "spacex", "nasa",
            "quantum physics", "particle physics", "fusion energy",
            "dark matter",
            "climate change", "carbon emissions", "renewable energy",
            "sustainability",
            "biotechnology", "genetics", "dna sequencing", "neuroscience",
            "gene editing",
            "materials science", "graphene", "nanotechnology",
            "artificial general intelligence", "brain computer interface",
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
            "data science", "software engineering",
        ],
        "related": [
            "chatgpt", "openai", "gpt", "gemini", "copilot",
            "llm", "ai model", "generative ai", "ai agent",
            "ai regulation", "ai safety", "transformer",
            "software", "hardware", "algorithm", "automation",
            "neural", "network", "chatbot", "api",
            "database", "server", "programming", "code", "developer",
            "web", "internet", "platform", "saas", "devops",
            "gpu", "chip", "semiconductor", "encryption", "malware",
            "firewall", "virtuali", "container", "microservice",
            "generative", "open source", "crypto", "robot",
            "digital", "cyber", "tech", "computing", "quantum",
            "data science", "computer security", "cloud native",
            "kubernetes", "docker", "edge computing", "5g", "iot",
        ],
    },
    "finance": {
        "core": [
            "stock market", "interest rate", "federal reserve",
            "monetary policy", "earnings report",
            "bitcoin", "ethereum", "crypto market", "defi",
            "digital payment", "fintech", "hedge fund", "etf",
            "forex trading", "asset management",
        ],
        "related": [
            "portfolio", "equity", "bond", "wealth",
            "forex", "inflation", "recession", "gdp",
            "dividend", "mortgage", "loan", "credit",
            "fiscal", "commodity", "valuation",
            "ipo", "wall street", "insurance",
            "stablecoin", "crypto regulation", "crypto trading",
            "crypto exchange", "web3 finance",
            "neobank", "robo-advisor", "regtech",
            "buy now pay later", "mobile payment",
            "contactless payment", "payment processing",
            "digital wallet", "payment gateway",
            "private equity", "capital market",
            "portfolio management", "risk management",
            "stock earnings", "quarterly earnings",
            "stock rally", "market crash",
            "bull market", "bear market", "stock valuation",
            "unemployment rate", "consumer price index",
            "cpi inflation", "interest rate hike",
            "fed rate decision", "economic outlook",
            "central bank", "derivatives", "nasdaq",
            "s&p", "dow jones",
        ],
    },
    "business": {
        "core": [
            "startup funding", "venture capital", "unicorn startup",
            "digital marketing", "content marketing", "marketing strategy",
            "business strategy", "corporate strategy",
            "supply chain", "digital transformation",
            "business automation", "ai in business",
        ],
        "related": [
            "startup", "entrepreneurship", "brand strategy",
            "commerce", "ecommerce", "retail", "logistics",
            "corporate", "venture", "customer", "market",
            "franchise", "merger", "acquisition", "stakeholder",
            "workforce", "hiring", "recruitment", "competitive",
            "outsourc", "consult", "b2b", "b2c", "crm",
            "partnership", "leadership", "pitch deck",
            "remote work", "gig economy", "creator economy",
            "seo", "social media marketing", "influencer marketing",
            "dropshipping", "shopify", "amazon seller",
            "saas", "unicorn", "ipo",
            "inventory management", "supply chain logistics",
        ],
    },
    "health": {
        "core": [
            "mental health", "public health", "medical research",
            "disease treatment", "telemedicine",
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
            "wearable", "health tech", "clinical trial",
            "mrna", "crispr", "longevity", "microbiome",
        ],
    },
    "science": {
        "core": [
            "quantum physics", "climate change",
            "space exploration", "biotechnology",
            "gene editing", "neuroscience",
        ],
        "related": [
            "research", "experiment", "energy",
            "solar", "nuclear", "genome",
            "biology", "chemistry", "physics",
            "renewable", "satellite", "carbon", "emission",
            "evolution", "ecosystem", "telescope", "particle",
            "molecule", "fossil", "biodiversity", "astro",
            "neurosci", "geolog", "planet", "nasa",
            "crispr", "fusion", "dark matter", "exoplanet",
            "graphene", "superconductor", "mars", "spacex",
        ],
    },
    "all categories": {"core": [], "related": []},
}

# ---------------------------------------------------------------------------
# Layer 3: Reusable exclusion building blocks
# ---------------------------------------------------------------------------
GEOGRAPHY_EXCLUSIONS = [
    "united states", "usa", "uk", "china", "india", "malaysia",
    "south korea", "north korea", "japan", "singapore",
    "europe", "africa", "asia", "london", "new york",
    "california", "texas", "county", "city", "province",
    "region", "state", "capital", "hong kong", "saudi arabia",
    "new zealand", "sri lanka", "costa rica", "puerto rico",
    "el salvador", "dominican republic", "czech republic",
    "ivory coast", "prefecture", "district",
]

EDUCATION_EXCLUSIONS = [
    "university", "college", "school", "academy",
    "student", "degree", "master", "phd", "course",
    "exam", "tuition", "campus", "faculty",
]

ENTERTAINMENT_EXCLUSIONS = [
    "movie", "film", "series", "tv show", "netflix",
    "celebrity", "actor", "actress", "singer",
    "music", "song", "album", "concert",
    "drama", "anime", "kpop", "hollywood",
]

SPORTS_EXCLUSIONS = [
    "football", "soccer", "basketball", "tennis",
    "fifa", "nba", "olympic", "cricket",
    "match", "tournament", "league",
]

LIFESTYLE_EXCLUSIONS = [
    "recipe", "cooking", "food", "restaurant",
    "fashion", "beauty", "makeup", "skincare",
    "travel", "hotel", "flight",
    "shopping", "discount", "sale",
    "prom dress", "white gold", "gold price",
]

ENGINEERING_EXCLUSIONS = [
    "power supply", "voltage", "current",
    "circuit", "watt", "amp", "electric",
    "battery", "resistor", "capacitor",
]

HEALTH_NOISE = [
    "weight loss", "diet plan", "workout",
    "exercise", "gym", "yoga", "meditation",
    "supplement", "vitamin",
]

NON_SCIENTIFIC = [
    "zodiac", "horoscope", "astrology",
    "fortune", "tarot", "prediction",
]

GENERIC_NOISE = [
    "wiki", "definition", "meaning",
    "example", "introduction",
    "history of", "what is",
    "brilliant math", "imdb",
    "religion", "church",
]

# Compose per-category exclusion lists from building blocks
DOMAIN_EXCLUSIONS = {
    "technology": [
        *GEOGRAPHY_EXCLUSIONS,
        *EDUCATION_EXCLUSIONS,
        *ENTERTAINMENT_EXCLUSIONS,
        *SPORTS_EXCLUSIONS,
        *LIFESTYLE_EXCLUSIONS,
        *ENGINEERING_EXCLUSIONS,
        *HEALTH_NOISE,
        *NON_SCIENTIFIC,
        *GENERIC_NOISE,
    ],
    "finance": [
        *GEOGRAPHY_EXCLUSIONS,
        *EDUCATION_EXCLUSIONS,
        *ENTERTAINMENT_EXCLUSIONS,
        *SPORTS_EXCLUSIONS,
        *LIFESTYLE_EXCLUSIONS,
        *ENGINEERING_EXCLUSIONS,
        *HEALTH_NOISE,
        *NON_SCIENTIFIC,
        *GENERIC_NOISE,
    ],
    "business": [
        *GEOGRAPHY_EXCLUSIONS,
        *EDUCATION_EXCLUSIONS,
        *ENTERTAINMENT_EXCLUSIONS,
        *SPORTS_EXCLUSIONS,
        *LIFESTYLE_EXCLUSIONS,
        *ENGINEERING_EXCLUSIONS,
        *HEALTH_NOISE,
        *NON_SCIENTIFIC,
        *GENERIC_NOISE,
    ],
    "health": [
        *GEOGRAPHY_EXCLUSIONS,
        *EDUCATION_EXCLUSIONS,
        *ENTERTAINMENT_EXCLUSIONS,
        *SPORTS_EXCLUSIONS,
        *LIFESTYLE_EXCLUSIONS,
        *ENGINEERING_EXCLUSIONS,
        # HEALTH_NOISE intentionally excluded — those topics are valid here
        *NON_SCIENTIFIC,
        *GENERIC_NOISE,
    ],
    "science": [
        *GEOGRAPHY_EXCLUSIONS,
        *EDUCATION_EXCLUSIONS,
        *ENTERTAINMENT_EXCLUSIONS,
        *SPORTS_EXCLUSIONS,
        *LIFESTYLE_EXCLUSIONS,
        # ENGINEERING_EXCLUSIONS intentionally excluded — physics/EE overlap
        *HEALTH_NOISE,
        *NON_SCIENTIFIC,
        *GENERIC_NOISE,
    ],
    "all categories": [
        *NON_SCIENTIFIC,
        *GENERIC_NOISE,
    ],
}

# ---------------------------------------------------------------------------
# Scoring parameters
# ---------------------------------------------------------------------------
TFIDF_SIMILARITY_THRESHOLD = 0.05
RELEVANCE_FLOOR = 0.15

RISING_SCORE_DEFAULT = 15

# ---------------------------------------------------------------------------
# Validation API routing — which sources apply to which category
# ---------------------------------------------------------------------------
VALIDATION_SOURCES = {
    "technology": ["news", "github", "stackexchange"],
    "finance":    ["news", "alphavantage"],
    "business":   ["news", "alphavantage"],
    "health":     ["news"],
    "science":    ["news", "github", "stackexchange"],
    "all categories": ["news"],
}

# Max bonus points each source can contribute
VALIDATION_MAX_BONUS = {
    "news":          5,
    "alphavantage":  5,
    "github":        5,
    "stackexchange": 5,
}

VALIDATION_TOTAL_CAP = 15

# ---------------------------------------------------------------------------
# Topic → Sub-category inference (keyword patterns per main category)
# First matching sub-category wins, so order from specific → general.
# ---------------------------------------------------------------------------
TOPIC_SUBCATEGORIES = {
    "technology": {
        "Artificial Intelligence": [
            "artificial intelligence", "machine learning", "deep learning",
            "chatgpt", "openai", "gpt", "gemini", "copilot", "claude",
            "llm", "neural", "transformer", "generative ai", "ai agent",
            "ai model", "ai regulation", "ai safety", "chatbot",
            "natural language processing", "computer vision", "diffusion",
            "midjourney", "stable diffusion", "anthropic", "mistral",
            "hugging face", "langchain", "perplexity", "deepseek",
            "language model", "large language", "neural network",
        ],
        "Cybersecurity": [
            "cybersecurity", "computer security", "encryption", "malware",
            "firewall", "ransomware", "phishing", "vulnerability",
            "cyber attack", "hacking", "data breach", "zero day",
            "penetration", "threat", "intrusion",
        ],
        "Hardware & Chips": [
            "gpu", "chip", "semiconductor", "processor",
            "hardware", "quantum computing", "quantum", "nvidia",
            "apple silicon",
        ],
        "Cloud & Infrastructure": [
            "cloud computing", "cloud native", "aws", "azure",
            "kubernetes", "docker", "microservice", "container",
            "serverless", "devops", "edge computing", "virtuali",
            "computing",
        ],
        "Blockchain & Crypto": [
            "blockchain", "crypto", "bitcoin", "ethereum",
            "defi", "nft", "web3", "smart contract", "token",
            "solana", "polygon", "blockchain technology",
        ],
        "Data & Analytics": [
            "data science", "big data", "analytics",
            "data mining", "data engineer", "data pipeline",
            "algorithm", "science",
        ],
        "Software Development": [
            "software", "programming", "developer",
            "github", "open source", "api", "framework",
            "database", "web development", "agile",
            "engineering", "computer science",
        ],
        "IoT & Connectivity": [
            "iot", "internet of things", "5g", "sensor",
            "smart home", "wearable", "robot",
        ],
        "Internet & Web": [
            "internet", "web", "browser", "website",
            "domain", "http", "url", "online platform",
            "search engine", "network",
        ],
    },
    "finance": {
        "Cryptocurrency": [
            "bitcoin", "ethereum", "crypto", "defi",
            "stablecoin", "token", "nft", "web3",
            "blockchain", "solana", "binance", "coinbase",
            "decentralized finance", "crypto market",
            "crypto trading", "crypto exchange", "crypto crash",
            "crypto regulation", "web3 finance",
        ],
        "Stock Market": [
            "stock", "nasdaq", "s&p", "dow jones", "equity",
            "ipo", "wall street", "bull market", "bear market",
            "stock earnings", "quarterly earnings",
            "stock rally", "market crash", "stock valuation",
            "earnings report", "share",
        ],
        "Banking & Lending": [
            "banking", "bank", "loan", "mortgage", "credit",
            "interest rate", "central bank", "federal reserve",
            "deposit",
        ],
        "Fintech": [
            "fintech", "digital payment", "neobank",
            "robo-advisor", "regtech", "insurtech", "stripe",
            "paypal", "square", "digital wallet",
            "mobile payment", "contactless payment",
            "payment processing", "payment gateway",
            "buy now pay later", "neobank fintech",
        ],
        "Investment": [
            "portfolio", "asset management", "fund",
            "hedge fund", "dividend", "wealth", "bond", "etf",
            "private equity", "capital market",
            "portfolio management", "risk management",
            "venture capital finance", "derivatives",
        ],
        "Economy": [
            "inflation", "recession", "gdp",
            "fiscal", "monetary policy", "employment",
            "tariff", "debt", "unemployment rate",
            "consumer price index", "cpi inflation",
            "interest rate hike", "fed rate decision",
            "economic outlook",
        ],
    },
    "business": {
        "Startups & VC": [
            "startup", "venture capital", "unicorn",
            "entrepreneurship", "pitch deck", "incubator",
            "accelerator", "seed round", "series a",
            "startup funding", "venture funding",
        ],
        "E-Commerce": [
            "ecommerce", "e-commerce", "commerce", "retail",
            "shopify", "amazon", "online shopping",
            "dropshipping", "amazon seller",
        ],
        "Marketing": [
            "digital marketing", "seo", "advertising",
            "social media marketing", "content marketing",
            "influencer marketing", "brand strategy",
            "branding", "marketing strategy",
        ],
        "Management & Leadership": [
            "corporate strategy", "leadership",
            "organizational management", "workforce",
            "hiring", "recruitment",
        ],
        "Supply Chain & Logistics": [
            "supply chain", "logistics", "shipping", "warehouse",
            "procurement", "inventory management",
            "supply chain logistics",
        ],
        "Digital Transformation": [
            "digital transformation", "business automation",
            "ai in business", "remote work",
            "gig economy", "creator economy",
        ],
    },
    "health": {
        "Mental Health": [
            "mental health", "anxiety", "depression", "therapy",
            "counseling", "mindfulness", "stress", "psychology",
        ],
        "Medical Research": [
            "medical research", "clinical trial", "vaccine",
            "pharma", "drug", "mrna", "crispr", "biotech",
        ],
        "Nutrition & Fitness": [
            "nutrition", "fitness", "diet", "supplement",
            "vitamin", "protein", "exercise", "workout",
        ],
        "Public Health": [
            "public health", "epidem", "pandemic", "virus",
            "infection", "outbreak", "cdc", "who",
        ],
        "Health Technology": [
            "telemedicine", "health tech", "wearable",
            "digital health", "remote monitoring", "ehr",
        ],
        "Disease & Treatment": [
            "cancer", "diabetes", "heart", "surgery",
            "treatment", "chronic", "immun", "diagnos",
        ],
    },
    "science": {
        "Space & Astronomy": [
            "space", "nasa", "spacex", "mars", "satellite",
            "telescope", "exoplanet", "rocket", "astro",
        ],
        "Climate & Environment": [
            "climate", "carbon", "emission", "renewable",
            "solar", "sustainability", "environment", "ecosystem",
        ],
        "Biotechnology": [
            "biotech", "gene", "crispr", "genome", "dna",
            "biology", "molecular", "cell", "protein",
        ],
        "Physics": [
            "quantum", "physics", "particle", "fusion",
            "dark matter", "superconductor", "graphene",
        ],
        "Earth Science": [
            "geolog", "fossil", "earthquake", "volcano",
            "ocean", "mineral", "planet",
        ],
        "Energy": [
            "renewable energy", "solar energy", "nuclear",
            "hydrogen", "battery", "fusion energy",
        ],
    },
    "all categories": {},
}
