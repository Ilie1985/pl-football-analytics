import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("FOOTBALL_DATA_TOKEN")

headers = {"X-Auth-Token": token}
url = "https://api.football-data.org/v4/competitions/PL"

r = requests.get(url, headers=headers)

print("Status:", r.status_code)
print(r.json())