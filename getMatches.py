
# Need previous fixtures for all teams and athletes
# Need upcoming fixtures for all teams and athletes 
# Need league tables (Prem rug and F1)

# TENNIS ATHLETES WILL HAVE TO BE DONE USING ESPN DB 

import requests
import json
import time


def previousTeamResults(teamID):
        url = f"https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id={teamID}"
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200 and res.text.strip():
                return res.json().get("results") or []
        except Exception:
            print("Error")
        return []
    
def previousMatches():
    #opening file
    with open("jsons/teams.json", "r") as f:
        teamDict = json.load(f)

    #Getting previous matches for all teams in the dictionary
    previousMatches = []
    for teamName, teamID in teamDict.items():
        teamPreviousMatches = previousTeamResults(teamID)
        previousMatches.extend(teamPreviousMatches)
        time.sleep(1.5)  # Add a delay between requests to avoid overwhelming the API

    # 3. Deduplicate events (in case two favorited teams played each other)
    uniquePreviousMatches = {m["idEvent"]: m for m in previousMatches if m.get("idEvent")}

    #sorting by date
    uniquePreviousMatches = list(uniquePreviousMatches.values())
    uniquePreviousMatches.sort(key=lambda x: x.get("dateEvent", ""), reverse=True)

    #Get the 10 most recent
    tenPreviousMatches = uniquePreviousMatches[:10]

    print(f"\n{'='*15} TOP 10 RECENT MATCHES {'='*15}\n")
    return tenPreviousMatches
    #for match in tenPreviousMatches:
    #    date = match.get("dateEvent") 
    #    hTeam = match.get("strHomeTeam")
    #    aTeam = match.get("strAwayTeam")
    #    hScore = match.get("intHomeScore")
    #    aScore = match.get("intAwayScore")
    #    league = match.get("strLeague")
    #    print(f"{date} | {league} | {hTeam} {hScore} - {aScore} {aTeam}")
       

def upcomingTeamResults(teamID):
        url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnext.php?id={teamID}"
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200 and res.text.strip():
                return res.json().get("events") or []
        except Exception:
            print("Error")
        return []

def upcomingMatches():
    #opening file
        with open("jsons/teams.json", "r") as f:
            teamDict = json.load(f)
    
        #Getting upcoming matches for all teams in the dictionary
        upcomingMatches = []
        for teamName, teamID in teamDict.items():
            teamUpcomingMatches = upcomingTeamResults(teamID)
            upcomingMatches.extend(teamUpcomingMatches)
            time.sleep(1.5)  # Add a delay between requests to avoid overwhelming the API
    
        # 3. Deduplicate events (in case two favorited teams played each other)
        uniqueUpcomingMatches = {m["idEvent"]: m for m in upcomingMatches if m.get("idEvent")}
    
        #sorting by date
        uniqueUpcomingMatches = list(uniqueUpcomingMatches.values())
        uniqueUpcomingMatches.sort(key=lambda x: x.get("dateEvent", ""), reverse=True)
    
        #Get the 10 most recent
        tenUpcomingMatches = uniqueUpcomingMatches[:10]
    
        print(f"\n{'='*15} TOP 10 UPCOMING MATCHES {'='*15}\n")
        return tenUpcomingMatches
        #for match in tenUpcomingMatches:
        #    date = match.get("dateEvent") 
        #    hTeam = match.get("strHomeTeam")
        #    aTeam = match.get("strAwayTeam")
        #    hScore = match.get("intHomeScore")
        #    aScore = match.get("intAwayScore")
        #    league = match.get("strLeague")
        #    print(f"{date} | {league} | {hTeam} {hScore} - {aScore} {aTeam}")

def main():
    prevMatches = previousMatches()
    upMatches = upcomingMatches()

    payload = {
        "Recent Matches": prevMatches,
        "Upcoming Matches": upMatches
    }

    with open("jsons/matches.json", "w") as f:
        json.dump(payload, f, indent=2)

    print("\nData has been written to matches.json")

main()