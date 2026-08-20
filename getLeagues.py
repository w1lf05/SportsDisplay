import requests

def get_f1_drivers_standings():
    url = "https://api.jolpi.ca/ergast/f1/current/driverstandings.json"
    res = requests.get(url, timeout=5)
    
    if res.status_code == 200:
        data = res.json()
        standings_lists = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
        if not standings_lists:
            return []
            
        driver_standings = standings_lists[0].get("DriverStandings", [])
        
        print(f"\n{'='*15} F1 DRIVERS' CHAMPIONSHIP {'='*15}\n")
        for driver in driver_standings:
            pos = driver.get("position")
            name = f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"
            team = driver["Constructors"][0]["name"] if driver.get("Constructors") else "N/A"
            points = driver.get("points")
            wins = driver.get("wins")
            print(f"{pos:>2}. {name:<22} ({team:<16}) Pts: {points:<4} Wins: {wins}")

get_f1_drivers_standings()