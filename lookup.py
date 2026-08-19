import requests

def lookup_events(event_ids):
    for event_id in event_ids:
        api_call = requests.get(f"https://www.thesportsdb.com/api/v1/json/123/lookupevent.php?id={event_id}")
        storage = api_call.json()
        for event in storage["events"]:
            date_event = event["dateEvent"]
            home_team = event["strHomeTeam"]
            home_team_id = event["idHomeTeam"]
            away_team = event["strAwayTeam"]
            away_team_id = event["idAwayTeam"]

        print(f"{date_event}: {home_team} (ID: {home_team_id}) vs {away_team} (ID: {away_team_id})")

def lookup_teams(team_ids):
    for team_id in team_ids:
        api_call = requests.get(f"https://www.thesportsdb.com/api/v1/json/123/searchteams.php?t={team_id}")
        storage = api_call.json()
        for team in storage["teams"]:
            team_name = team["strTeam"]
            team_stadium = team["strStadium"]

        print(f"{team_name} plays at {team_stadium}.")

def lookup_leagues(league_ids):
    for league_id in league_ids:
        api_call = requests.get(f"https://www.thesportsdb.com/api/v1/json/123/lookupleague.php?id={league_id}")
        storage = api_call.json()
        for league in storage["leagues"]:
            league_name = league["strLeague"]
            league_country = league["strCountry"]

        print(f"{league_name} is based in {league_country}.")


def get_team_ids(team_names):
    for team_name in team_names:
        url = "https://www.thesportsdb.com/api/v1/json/3/searchteams.php"
        response = requests.get(url, params={"t": team_name})
            
        if response.status_code == 200 and response.text.strip():
            data = response.json()
            teams = data.get("teams")
            if teams:
                for team in teams:
                    print(f"Name: {team.get('strTeam')} | ID: {team.get('idTeam')} | League: {team.get('strLeague')} (ID: {team.get('idLeague')})")
            else:
                print(f"No results found for '{team_name}'.")

def lookup_players(player_names):
    for player_name in player_names:
        url = "https://www.thesportsdb.com/api/v1/json/123/searchplayers.php"
        response = requests.get(url, params={"p": player_name})

        if response.status_code == 200 and response.text.strip():
            data = response.json()
            players = data.get("player")
            if players:
                for player in players:
                    print(f"Name: {player.get('strPlayer')} | ID: {player.get('idPlayer')} | Team: {player.get('strTeam')} | Position: {player.get('strPosition')}")
            else:
                print(f"No results found for '{player_name}'.")
            player_team = player["strTeam"]
            player_position = player["strPosition"]
            player_id = player["idPlayer"]

        print(f"{player_name} (ID: {player_id}) plays for {player_team} as a {player_position}.")

    

event_ids = [2551089]
team_ids = ["Arsenal", "Chelsea", "Liverpool"]
league_ids = [4328, 4329, 4330, 4331]
player_names = ["Emma Raducanu", "Ronnie O'Sullivan", "Jack Draper"]

team_names = ["McLaren Formula 1 Team", "Harlequins"]


#Got to do internationals 
#Got to do players such as tennis and snooker
# Got to do leagues such as f1 and prem rug to see all




#lookup_events(event_ids)
#lookup_teams(team_ids)
#lookup_leagues(league_ids)
#get_team_ids(team_names)
lookup_players(player_names)
