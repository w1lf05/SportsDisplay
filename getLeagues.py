import requests
import json

## As the free tier of the sportsDB doesnt allow most recent leagues that arent football, I have to use separate APIs

def get_f1_drivers_standings():
    url = "https://api.jolpi.ca/ergast/f1/current/driverstandings.json"
    res = requests.get(url, timeout=5)
    
    if res.status_code == 200:
        data = res.json()
        standings_lists = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
        if not standings_lists:
            return []
            
        driver_standings = standings_lists[0].get("DriverStandings", [])

        return driver_standings
        



def get_f1_constructor_standings():
    url = "https://api.jolpi.ca/ergast/f1/current/constructorStandings.json"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            standings = data["MRData"]["StandingsTable"]["StandingsLists"][0]

        return standings

    except Exception as e:
        print(f"Error fetching F1 constructor standings: {e}")

    return {}


def get_premiership_rugby_table(season=None):
    url = "https://site.api.espn.com/apis/v2/sports/rugby/rugby-union/leagues/eng.1/standings"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            children = data.get("children") or []
            if children:
                entries = data.get("children", [{}])[0].get("standings", {}).get("entries", [])
            else:
                entries = data.get("standings", {}).get("entries", [])

        # 3. Parse entries into table records
        table = []
        for idx, item in enumerate(entries, start=1):
            team_name = item.get("team", {}).get("displayName", "Unknown")
            stats_list = item.get("stats", [])
            stats = {s.get("name"): s.get("value") for s in stats_list}

            table.append(
                {
                    "pos": idx,
                    "team": team_name,
                    "played": int(stats.get("gamesPlayed", 0)),
                    "wins": int(stats.get("wins", 0)),
                    "ties": int(stats.get("ties", 0)),
                    "losses": int(stats.get("losses", 0)),
                    "diff": int(
                        stats.get(
                            "pointDifferential", stats.get("pointsDiff", 0)
                        )
                    ),
                    "pts": int(stats.get("points", 0)),
                }
            )

        return table

    except Exception as e:
        print(f"Error fetching Premiership Rugby table: {e}")
        return []

def main():

    standings = get_f1_constructor_standings()
    season = standings.get("season")
    constructors = standings.get("ConstructorStandings", [])
    
    drivers = get_f1_drivers_standings()

    payload = {
        "Drivers Standings": drivers,
        "Constructors Standings": constructors,
        "Prem Rugby Standings": get_premiership_rugby_table()
    }

    with open("jsons/leagueTables.json", "w") as f:
        json.dump(payload, f, indent=2)

    print("\nData has been written to leagueTables.json")

    #print(f"\n{'=' * 15} F1 CONSTRUCTOR STANDINGS ({season}) {'=' * 15}")
    #print(f"{'Pos':<4} {'Constructor':<25} {'Wins':>5} {'Pts':>6}")
    #print("-" * 45)
    #for c in constructors:
    #    pos = c.get("position")
    #    name = c["Constructor"]["name"]
    #    wins = c.get("wins")
    #    pts = c.get("points")
    #    print(f"{pos:<4} {name:<25} {wins:>5} {pts:>6}")
#
    #print(f"\n{'='*15} F1 DRIVERS' CHAMPIONSHIP {'='*15}\n")
    #for driver in drivers:
    #    pos = driver.get("position")
    #    name = f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"
    #    team = driver["Constructors"][0]["name"] if driver.get("Constructors") else "N/A"
    #    points = driver.get("points")
    #    wins = driver.get("wins")
    #    print(f"{pos:>2}. {name:<22} ({team:<16}) Pts: {points:<4} Wins: {wins}")

if __name__ == "__main__":
    main()