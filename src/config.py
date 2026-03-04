import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("FOOTBALL_DATA_TOKEN")
BASE_URL = "https://api.football-data.org/v4"
COMPETITION_CODE = "PL"

if not API_TOKEN:
    raise RuntimeError(
        "Missing FOOTBALL_DATA_TOKEN. Create a .env file with:\n"
        "FOOTBALL_DATA_TOKEN=your_token_here"
    )