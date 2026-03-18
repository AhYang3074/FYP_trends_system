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
        "bnpl": "buy now pay later",
        # Standalone fragments → full concept (exact match only)
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
        "federal reserve bank": "federal reserve",
        "federal reserve system": "federal reserve",
    }

    # L1.5 — too-broad standalone topics (exact match, post-normalize)
    GENERIC_TOPICS = {
        # Tech
        "technology", "software", "internet", "science",
        "data", "system", "platform", "application",
        "network", "computer", "engineering", "computing",
        "information", "digital", "security", "analysis",
        "language", "version", "protocol", "architecture",
        "structure", "framework", "method", "technique",
        "concept", "theory", "resource", "device",
        # Business
        "management", "research", "development", "design",
        "process", "model", "program", "solution",
        "strategy", "marketing", "innovation", "funding",
        "operation", "performance", "optimization", "growth",
        "revenue", "profit", "industry", "sector",
        "regulation", "compliance", "governance",
        "leadership", "pitch book",
        # Finance
        "payment", "market", "earnings", "finance",
        "investment", "cryptocurrency", "trading", "banking",
        "economy", "rate", "policy", "exchange",
        "valuation", "monetary", "hedge", "equity",
        "bond", "asset", "portfolio", "capital",
        "derivative", "commodity", "inflation", "interest",
        "credit", "loan", "mortgage", "dividend",
        "fiscal", "wealth", "insurance", "forex",
        "fund", "index", "yield", "liquidity",
        # Multi-word static concepts (not trends)
        "interest rate", "monetary policy", "federal reserve",
        "hedge fund", "stock market", "central bank",
        "fiscal policy", "monetary system",
        "neobank", "recession",
    }

    # L1.5 — temporal / seasonal noise (substring match)
    TEMPORAL_NOISE = [
        "summer", "winter", "spring", "fall",
        "autumn", "holiday", "festival", "event",
        "christmas", "halloween", "new year",
        "black friday", "cyber monday", "valentine",
    ]

    # Trend-signal words → dynamic topics get a score boost
    TREND_PATTERNS = [
        "crash", "surge", "hike", "drop", "rally",
        "crisis", "boom", "bubble", "plunge", "soar",
        "breakout", "collapse", "spike", "dip", "price",
        "forecast", "prediction", "outlook", "warning",
        "decision", "announcement", "launch", "release",
        "ban", "hack", "breach", "attack",
        "disruption", "shortage", "layoff", "bankruptcy",
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
        "defi": "DeFi",
        "web3": "Web3",
        "midjourney": "Midjourney",
        "copilot": "Copilot",
        "claude": "Claude",
        "gemini": "Gemini",
        "anthropic": "Anthropic",
        "mistral": "Mistral",
        "langchain": "LangChain",
        "perplexity": "Perplexity",
        "bitcoin": "Bitcoin",
        "ethereum": "Ethereum",
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
        "federal reserve": "Federal Reserve",
        "etf": "ETF",
        "ipo": "IPO",
        "gdp": "GDP",
        "cpi inflation": "CPI Inflation",
        "s&p 500": "S&P 500",
        "buy now pay later": "Buy Now Pay Later",
        "nasdaq": "NASDAQ",
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

    # --- Layer 1.5: Generic / temporal filter (runs on normalized name) ---
    @staticmethod
    def is_noise(name):
        if name in TopicProcessor.GENERIC_TOPICS:
            return True
        if any(t in name for t in TopicProcessor.TEMPORAL_NOISE):
            return True
        return False

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

    # --- Trend dynamism boost ---
    @staticmethod
    def trend_boost(name):
        """Flat +10 bonus for topics with action/event words."""
        if any(p in name for p in TopicProcessor.TREND_PATTERNS):
            return 10
        return 0

    # --- Display name (proper casing) ---
    @staticmethod
    def display_name(name):
        if name in TopicProcessor.DISPLAY_NAMES:
            return TopicProcessor.DISPLAY_NAMES[name]
        return name.title()
