import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

DEFAULT_CATEGORY = 18
DEFAULT_DATE_RANGE = "today 1-m"
