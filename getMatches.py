import json
from pathlib import Path
import time
import requests

JSONS_DIR = Path(__file__).resolve().parent / "jsons"
JSONS_DIR.mkdir(exist_ok=True)


def fetch_previous_team_results(team_id, team_name, retries=2):
    """Fetches the last 5 completed matches for a given team ID."""
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id={team_id}"

    for attempt in range(1, retries + 1):
        try:
            res = requests.get(url, timeout=8)
            if res.status_code == 200 and res.text.strip():
                data = res.json()
                return data.get("results") or []
            elif res.status_code == 429:
                print(
                    f"  ⚠️ Rate limit (429) on {team_name}. Retrying"
                )
                time.sleep(100)
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Network error on {team_name}: {e}")
            time.sleep(1)

    return []


def fetch_upcoming_team_results(team_id, team_name, retries=2):
    """Fetches the next 5 scheduled matches for a given team ID."""
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnext.php?id={team_id}"

    for attempt in range(1, retries + 1):
        try:
            res = requests.get(url, timeout=8)
            if res.status_code == 200 and res.text.strip():
                data = res.json()
                return data.get("events") or []
            elif res.status_code == 429:
                print(
                    f"  ⚠️ Rate limit (429) on {team_name}. Retrying in 2s..."
                )
                time.sleep(2)
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Network error on {team_name}: {e}")
            time.sleep(1)

    return []


def get_all_previous_matches(team_dict):
    all_results = []
    print(f"\n--- Fetching Recent Matches for {len(team_dict)} Teams ---")

    for i, (team_name, team_id) in enumerate(team_dict.items(), start=1):
        matches = fetch_previous_team_results(team_id, team_name)
        all_results.extend(matches)
        print(f"[{i}/{len(team_dict)}] {team_name}: Found {len(matches)} past matches")
        time.sleep(2)  # Delay between requests to avoid errors

    # Deduplicate by idEvent
    unique_matches = {m["idEvent"]: m for m in all_results if m.get("idEvent")}

    # Sort descending: Most recent first
    sorted_matches = sorted(
        unique_matches.values(),
        key=lambda x: x.get("dateEvent", ""),
        reverse=True,
    )

    return sorted_matches[:10]


def get_all_upcoming_matches(team_dict):
    all_events = []
    print(f"\n--- Fetching Upcoming Fixtures for {len(team_dict)} Teams ---")

    for i, (team_name, team_id) in enumerate(team_dict.items(), start=1):
        events = fetch_upcoming_team_results(team_id, team_name)
        all_events.extend(events)
        print(f"[{i}/{len(team_dict)}] {team_name}: Found {len(events)} upcoming fixtures")
        time.sleep(2)

    # Deduplicate by idEvent
    unique_events = {m["idEvent"]: m for m in all_events if m.get("idEvent")}

    # Sort ascending: Closest chronological fixture first
    sorted_events = sorted(
        unique_events.values(),
        key=lambda x: x.get("dateEvent", ""),
        reverse=False,
    )

    return sorted_events[:10] 


def main():
    teams_file = JSONS_DIR / "teams.json"
    matches_file = JSONS_DIR / "matches.json"

    if not teams_file.exists():
        print(f"Error: {teams_file} not found.")
        return

    with open(teams_file, "r", encoding="utf-8") as f:
        team_dict = json.load(f)

    # Load existing cache to protect against failed runs
    cached_payload = {"Recent Matches": [], "Upcoming Matches": []}
    if matches_file.exists():
        try:
            with open(matches_file, "r", encoding="utf-8") as f:
                cached_payload = json.load(f)
        except Exception:
            pass

    prev_matches = get_all_previous_matches(team_dict)
    up_matches = get_all_upcoming_matches(team_dict)

    # Guard: Fall back to existing cached data if a fetch returned 0 results due to network issues
    final_prev = (
        prev_matches
        if prev_matches
        else cached_payload.get("Recent Matches", [])
    )
    final_up = (
        up_matches if up_matches else cached_payload.get("Upcoming Matches", [])
    )

    payload = {
        "Recent Matches": final_prev,
        "Upcoming Matches": final_up,
    }

    with open(matches_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(
        f"\n✅ Updated matches.json with {len(final_prev)} past and {len(final_up)} upcoming matches."
    )


if __name__ == "__main__":
    main()