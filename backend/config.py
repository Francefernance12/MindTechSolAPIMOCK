import os
from dotenv import load_dotenv

load_dotenv()  # reads .env into os.environ automatically

API_KEY    = os.environ.get("API_KEY")
RATE_LIMIT = os.environ.get("RATE_LIMIT", "30 per minute")

if not API_KEY:
    raise RuntimeError("API_KEY environment variable is not set.")