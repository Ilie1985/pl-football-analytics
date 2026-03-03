import json
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def season_label_from_filename(path: Path) -> str:
    # examples: matches_PL_2023.json -> 2023, matches_PL_current.json -> current
    parts = path.stem.split("_")
    return parts[-1]

def clean_matches(files: list[Path]) -> pd.DataFrame:
    frames = []

    for f in files:
        label = season_label_from_filename(f)
        data = load_json(f)

        df = pd.json_normalize(data.get("matches", []))
        if df.empty:
            continue

        # keep important columns (some may be missing depending on endpoint)
        wanted = [
            "id",
            "utcDate",
            "status",
            "matchday",
            "homeTeam.id",
            "homeTeam.name",
            "awayTeam.id",
            "awayTeam.name",
            "score.fullTime.home",
            "score.fullTime.away",
        ]
        existing = [c for c in wanted if c in df.columns]
        df = df[existing].copy()

        rename = {
            "id": "match_id",
            "utcDate": "utc_date",
            "status": "status",
            "matchday": "matchday",
            "homeTeam.id": "home_team_id",
            "homeTeam.name": "home_team",
            "awayTeam.id": "away_team_id",
            "awayTeam.name": "away_team",
            "score.fullTime.home": "ft_home",
            "score.fullTime.away": "ft_away",
        }
        df = df.rename(columns=rename)

        df["season_label"] = label
        df["utc_date"] = pd.to_datetime(df["utc_date"], errors="coerce", utc=True)

        # scores can be null for scheduled matches
        df["ft_home"] = pd.to_numeric(df.get("ft_home"), errors="coerce")
        df["ft_away"] = pd.to_numeric(df.get("ft_away"), errors="coerce")

        df["total_goals"] = df["ft_home"] + df["ft_away"]
        df["goal_diff_home"] = df["ft_home"] - df["ft_away"]

        def result(row):
            if pd.isna(row["ft_home"]) or pd.isna(row["ft_away"]):
                return None
            if row["ft_home"] > row["ft_away"]:
                return "H"
            if row["ft_home"] < row["ft_away"]:
                return "A"
            return "D"

        df["result"] = df.apply(result, axis=1)

        frames.append(df)

    if not frames:
        return pd.DataFrame()

    out = pd.concat(frames, ignore_index=True)

    # helpful extra columns
    out["date"] = out["utc_date"].dt.date
    out["year"] = out["utc_date"].dt.year
    out["month"] = out["utc_date"].dt.month

    return out

def clean_scorers(files: list[Path]) -> pd.DataFrame:
    frames = []

    for f in files:
        label = season_label_from_filename(f)
        data = load_json(f)

        df = pd.json_normalize(data.get("scorers", []))
        if df.empty:
            continue

        possible_cols = [
            "player.id", "player.name",
            "team.id", "team.name",
            "goals", "assists", "penalties"
        ]
        cols = [c for c in possible_cols if c in df.columns]
        df = df[cols].copy()

        df["season_label"] = label

        df = df.rename(columns={
            "player.id": "player_id",
            "player.name": "player_name",
            "team.id": "team_id",
            "team.name": "team_name",
        })

        frames.append(df)

    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

def clean_standings(files: list[Path]) -> pd.DataFrame:
    frames = []

    for f in files:
        label = season_label_from_filename(f)
        data = load_json(f)

        standings = data.get("standings", [])
        total = next((s for s in standings if s.get("type") == "TOTAL"), None)
        if not total:
            continue

        rows = []
        for entry in total.get("table", []):
            rows.append({
                "season_label": label,
                "position": entry.get("position"),
                "team_id": entry.get("team", {}).get("id"),
                "team": entry.get("team", {}).get("name"),
                "played": entry.get("playedGames"),
                "won": entry.get("won"),
                "draw": entry.get("draw"),
                "lost": entry.get("lost"),
                "gf": entry.get("goalsFor"),
                "ga": entry.get("goalsAgainst"),
                "gd": entry.get("goalDifference"),
                "points": entry.get("points"),
                "form": entry.get("form"),
            })

        frames.append(pd.DataFrame(rows))

    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

def main():
    match_files = sorted(RAW_DIR.glob("matches_PL_*.json"))
    scorer_files = sorted(RAW_DIR.glob("scorers_PL_*.json"))
    standing_files = sorted(RAW_DIR.glob("standings_PL_*.json"))

    matches = clean_matches(match_files)
    scorers = clean_scorers(scorer_files)
    standings = clean_standings(standing_files)

    # Save full (includes scheduled games)
    matches.to_csv(OUT_DIR / "matches.csv", index=False)
    scorers.to_csv(OUT_DIR / "scorers.csv", index=False)
    standings.to_csv(OUT_DIR / "standings.csv", index=False)

    # Save modelling-ready (finished only)
    if not matches.empty and "status" in matches.columns:
        finished = matches[matches["status"] == "FINISHED"].copy()
        finished.to_csv(OUT_DIR / "matches_finished.csv", index=False)

    print("Saved:")
    print(" - data/processed/matches.csv")
    print(" - data/processed/matches_finished.csv (FINISHED only)")
    print(" - data/processed/scorers.csv")
    print(" - data/processed/standings.csv")

if __name__ == "__main__":
    main()