import json
from pathlib import Path
from datetime import date

from src.config import API_TOKEN, BASE_URL, COMPETITION_CODE
from src.api_client import FootballDataClient

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def save_json(data, filepath: Path) -> None:
    filepath.write_text(json.dumps(data, indent=2), encoding="utf-8")

def safe_get(client, path, params, out_path):
    try:
        data = client.get(path, params=params)
        save_json(data, out_path)
        print(f"Saved {out_path.name}")
        return True
    except Exception as e:
        print(f"[WARN] {out_path.name}: {e}")
        return False

def main():
    client = FootballDataClient(BASE_URL, API_TOKEN)

    # 1) Always fetch CURRENT season (no season parameter)
    print("=== CURRENT SEASON (no season param) ===")
    safe_get(client, f"/competitions/{COMPETITION_CODE}/matches", None,
             RAW_DIR / f"matches_{COMPETITION_CODE}_current.json")
    safe_get(client, f"/competitions/{COMPETITION_CODE}/scorers", None,
             RAW_DIR / f"scorers_{COMPETITION_CODE}_current.json")
    safe_get(client, f"/competitions/{COMPETITION_CODE}/standings", None,
             RAW_DIR / f"standings_{COMPETITION_CODE}_current.json")

    # 2) Try historical seasons (will be skipped if restricted)
    current_year = date.today().year
    seasons = list(range(current_year - 5, current_year))  # last 5 start years
    print(f"\n=== HISTORICAL SEASONS attempt: {seasons} ===")

    for season in seasons:
        print(f"\n--- Season {season} ---")
        ok = safe_get(
            client,
            f"/competitions/{COMPETITION_CODE}/matches",
            {"season": season},
            RAW_DIR / f"matches_{COMPETITION_CODE}_{season}.json"
        )
        if not ok:
            # If matches restricted, scorers/standings likely restricted too; skip fast
            continue

        safe_get(client, f"/competitions/{COMPETITION_CODE}/scorers", {"season": season},
                 RAW_DIR / f"scorers_{COMPETITION_CODE}_{season}.json")
        safe_get(client, f"/competitions/{COMPETITION_CODE}/standings", {"season": season},
                 RAW_DIR / f"standings_{COMPETITION_CODE}_{season}.json")

    print("\nDone. Check data/raw/")

if __name__ == "__main__":
    main()