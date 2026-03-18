import re
from utils.config import DOMAIN_KEYWORDS, DOMAIN_EXCLUSIONS, TOPIC_SUBCATEGORIES


class TopicProcessor:
    # L1 — single-word noise (exact match, pre-normalize)
    GENERIC_WORDS = {
        "news", "price", "data", "review", "update", "latest",
        "best", "top", "free", "online", "download", "app",
        "website", "tool", "service", "company", "stock",
        "video", "photo", "image", "map", "list", "guide",
        "today", "near me", "login", "sign up",
        "mobile", "phone", "device", "product", "account",
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
        # Standalone fragments → full concept
        "intelligence": "artificial intelligence",
        "machine": "machine learning",
        "learning": "machine learning",
        "cyber": "cybersecurity",
        "blockchain": "blockchain technology",
        "cloud": "cloud computing",
        "inventory": "inventory management",
        "logistics": "supply chain",
        "supply chain logistics": "supply chain",
        "branding": "brand strategy",
        "automation": "business automation",
        "unicorn": "unicorn startup",
        # Finance merges
        "earnings": "earnings report",
        "cryptocurrency": "crypto market",
        "bitcoin": "crypto market",
        "stablecoin": "crypto market",
        "decentralized finance": "crypto market",
        "defi": "crypto market",
        "federal reserve bank": "federal reserve",
        "federal reserve system": "federal reserve",
        "central bank": "federal reserve",
        "monetary policy": "federal reserve",
    }

    # L1.5 — too-broad standalone topics (exact match, post-normalize)
    GENERIC_TOPICS = {
        "technology", "software", "internet", "science",
        "data", "system", "platform", "application",
        "network", "computer", "engineering", "computing",
        "information", "digital", "security", "analysis",
        "management", "research", "development", "design",
        "process", "model", "program", "solution",
        "language", "version", "protocol", "architecture",
        "structure", "framework", "method", "technique",
        "concept", "theory", "resource", "device",
        "strategy", "marketing", "innovation", "funding",
        "operation", "performance", "optimization", "growth",
        "revenue", "profit", "industry", "sector",
        "regulation", "compliance", "governance",
        "leadership", "pitch book",
        "finance", "investment", "trading", "banking",
        "economy", "asset", "wealth", "bond",
        "equity", "commodity", "currency",
        "policy", "rate", "consumer", "fund",
        "financial market", "stock market", "investment fund",
        "neobank fintech",
        "digital payment", "mobile banking",
        "mobile phone", "mobile device", "phone",
        "financial technology", "foreign exchange market",
        "earnings report",
    }

    # L1.5 — temporal / seasonal noise (substring match)
    TEMPORAL_NOISE = [
        "summer", "winter", "spring", "fall",
        "autumn", "holiday", "festival", "event",
        "christmas", "halloween", "new year",
        "black friday", "cyber monday", "valentine",
    ]

    # Single-word topics that are allowed (known products/brands)
    ALLOW_SINGLE = {
        # Tech products
        "chatgpt", "openai", "deepseek", "gemini", "copilot", "claude",
        "midjourney", "anthropic", "mistral", "perplexity",
        "kubernetes", "docker", "tensorflow", "pytorch",
        "nvidia", "shopify", "nasdaq",
        # Crypto (after merge these become multi-word, but keep as safety)
        "coinbase", "binance", "solana",
    }

    # Trend signal words — topics containing these get a scoring bonus
    TREND_WORDS = [
        "crash", "surge", "rally", "hike", "cut",
        "decision", "crisis", "boom", "bubble", "disruption",
        "breakthrough", "ban", "launch", "shutdown",
    ]

    # Display-name overrides for proper casing
    DISPLAY_NAMES = {
        "chatgpt": "ChatGPT",
        "openai": "OpenAI",
        "deepseek": "DeepSeek",
        "gpt": "GPT",
        "llm": "LLM",
        "api": "API",
        "aws": "AWS",
        "saas": "SaaS",
        "devops": "DevOps",
        "github": "GitHub",
        "stackoverflow": "StackOverflow",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "mongodb": "MongoDB",
        "mysql": "MySQL",
        "postgresql": "PostgreSQL",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "nvidia": "NVIDIA",
        "iot": "IoT",
        "5g": "5G",
        "nft": "NFT",
        "web3": "Web3",
        "midjourney": "Midjourney",
        "copilot": "Copilot",
        "claude": "Claude",
        "gemini": "Gemini",
        "anthropic": "Anthropic",
        "mistral": "Mistral",
        "langchain": "LangChain",
        "perplexity": "Perplexity",
        "solana": "Solana",
        "paypal": "PayPal",
        "coinbase": "Coinbase",
        "cybersecurity": "Cybersecurity",
        "blockchain technology": "Blockchain Technology",
        "cryptocurrency wallet": "Cryptocurrency Wallet",
        "unicorn startup": "Unicorn Startup",
        "inventory management": "Inventory Management",
        "brand strategy": "Brand Strategy",
        "business automation": "Business Automation",
        "ai in business": "AI in Business",
        "seo": "SEO",
        "crm": "CRM",
        "b2b": "B2B",
        "b2c": "B2C",
        "ecommerce": "eCommerce",
        "etf": "ETF",
        "bnpl": "BNPL",
        "gdp": "GDP",
        "cpi inflation": "CPI Inflation",
        "ipo": "IPO",
        "s&p 500": "S&P 500",
        "neobank fintech": "Neobank Fintech",
        "crypto market": "Crypto Market",
        "digital payment": "Digital Payment",
        "financial market": "Financial Market",
        "earnings report": "Earnings Report",
        "federal reserve": "Federal Reserve",
    }

    _DOMAIN_RE = re.compile(r"\.(com|org|net|io|ai|co|gov|edu)\b")

    # --- Layer 1: Basic Cleaning ---
    @staticmethod
    def clean(name):
        name = name.lower().strip()
        name = TopicProcessor._DOMAIN_RE.sub("", name).strip()
        if not name or len(name) < 2:
            return None
        if name in TopicProcessor.GENERIC_WORDS:
            return None
        return name

    @staticmethod
    def normalize(name):
        return TopicProcessor.REPLACEMENTS.get(name, name)

    # --- Layer 1.5: Noise filter (runs on normalized name) ---
    @staticmethod
    def is_noise(name):
        if name in TopicProcessor.GENERIC_TOPICS:
            return True
        if any(t in name for t in TopicProcessor.TEMPORAL_NOISE):
            return True
        if len(name.split()) <= 1 and name not in TopicProcessor.ALLOW_SINGLE:
            return True
        return False

    # --- Scoring signals ---
    @staticmethod
    def has_trend_signal(name):
        return any(w in name for w in TopicProcessor.TREND_WORDS)

    MACRO_KEYWORDS = [
        "federal reserve", "interest rate", "inflation",
        "recession", "gdp", "fed rate", "cpi",
    ]

    @staticmethod
    def signal_bonus(name, subcategory=""):
        """Extra points for macro/crypto/event signals, penalty for fintech."""
        bonus = 0
        if any(k in name for k in TopicProcessor.MACRO_KEYWORDS):
            bonus += 15
        if any(w in name for w in TopicProcessor.TREND_WORDS):
            bonus += 10
        if "crypto" in name or "bitcoin" in name or "defi" in name:
            bonus += 10
        if subcategory == "Fintech":
            bonus -= 10
        return bonus

    # --- Layer 2: Keyword match score (continuous) ---
    @staticmethod
    def keyword_match_score(name, category_name):
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
        subcats = TOPIC_SUBCATEGORIES.get(category_name.lower(), {})
        for subcat, patterns in subcats.items():
            if any(p in name for p in patterns):
                return subcat
        return "General"

    # --- Display name (proper casing) ---
    @staticmethod
    def display_name(name):
        if name in TopicProcessor.DISPLAY_NAMES:
            return TopicProcessor.DISPLAY_NAMES[name]
        return name.title()
