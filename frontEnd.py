import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import getLeagues, getMatches

# File paths
BASE_DIR = Path(__file__).resolve().parent
JSONS_DIR = BASE_DIR / "jsons"


def run_all_updates():
    print(" Updating JSON files...")
    getMatches.main()
    getLeagues.main()
    print(" JSON files updated.")


def matchesTab(notebook):
    # --- Matches Tab Container ---
    matchesFrame = tk.Frame(notebook, bg="#1e293b")
    notebook.add(matchesFrame, text="Matches")

    # Force exact 50/50 vertical division between row 0 and row 1
    matchesFrame.columnconfigure(0, weight=1)
    matchesFrame.rowconfigure(0, weight=1, uniform="matches_half")
    matchesFrame.rowconfigure(1, weight=1, uniform="matches_half")

    # Load match data safely
    matches_data = {}
    matches_file = JSONS_DIR / "matches.json"
    if matches_file.exists():
        try:
            with open(matches_file, "r", encoding="utf-8") as f:
                matches_data = json.load(f)
        except Exception as e:
            print(f"Error loading matches.json: {e}")

    # ================= 1. UPCOMING MATCHES (TOP HALF - 50%) =================
    upcomingBox = tk.LabelFrame(
        matchesFrame,
        text=" Upcoming Matches ",
        font=("Segoe UI", 9, "bold"),
        fg="#38bdf8",
        bg="#1e293b",
        bd=1,
        relief="solid",
    )
    upcomingBox.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

    upcomingMatchesText = tk.Text(
        upcomingBox,
        bg="#1e293b",
        fg="white",
        font=("Consolas", 8),
        bd=0,
        wrap="word",
    )
    upcomingMatchesText.pack(fill="both", expand=True, padx=8, pady=6)

    upcoming_list = matches_data.get("Upcoming Matches", [])
    if not upcoming_list:
        upcomingMatchesText.insert("end", "No upcoming fixtures scheduled.\n")
    else:
        for match in upcoming_list:
            date = match.get("dateEvent", "")
            time_str = match.get("strTime", "")
            league = match.get("strLeague", "")
            hTeam = match.get("strHomeTeam", "")
            aTeam = match.get("strAwayTeam", "")
            time_display = f" | {time_str[:5]}" if time_str else ""

            upcomingMatchesText.insert(
                "end",
                f"{date}{time_display} | {league}\n  {hTeam} vs {aTeam}\n\n",
            )

    # ================= 2. RECENT RESULTS (BOTTOM HALF - 50%) =================
    recentBox = tk.LabelFrame(
        matchesFrame,
        text=" Recent Results ",
        font=("Segoe UI", 9, "bold"),
        fg="#38bdf8",
        bg="#1e293b",
        bd=1,
        relief="solid",
    )
    recentBox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

    recentMatchesText = tk.Text(
        recentBox,
        bg="#1e293b",
        fg="white",
        font=("Consolas", 8),
        bd=0,
        wrap="word",
    )
    recentMatchesText.pack(fill="both", expand=True, padx=8, pady=6)

    recent_list = matches_data.get("Recent Matches", [])
    if not recent_list:
        recentMatchesText.insert("end", "No recent match records found.\n")
    else:
        for match in recent_list:
            date = match.get("dateEvent", "")
            league = match.get("strLeague", "")
            hTeam = match.get("strHomeTeam", "")
            aTeam = match.get("strAwayTeam", "")
            hScore = match.get("intHomeScore", "-")
            aScore = match.get("intAwayScore", "-")

            recentMatchesText.insert(
                "end",
                f"{date} | {league}\n  {hTeam} {hScore} - {aScore} {aTeam}\n\n",
            )

def leaguesTab(notebook):
    # --- Consolidated Tables / Leagues Container ---
    leaguesFrame = tk.Frame(notebook, bg="#1e293b")
    notebook.add(leaguesFrame, text="🏆 Standings")

    # Grid configuration:
    # 2 equal columns (50% / 50%)
    leaguesFrame.columnconfigure(0, weight=1, uniform="col")
    leaguesFrame.columnconfigure(1, weight=1, uniform="col")
    # 2 equal rows (50% top half, 50% bottom half)
    leaguesFrame.rowconfigure(0, weight=1, uniform="row")
    leaguesFrame.rowconfigure(1, weight=1, uniform="row")

    league_file = JSONS_DIR / "leagueTables.json"
    leagueTables = {}
    if league_file.exists():
        try:
            with open(league_file, "r", encoding="utf-8") as f:
                leagueTables = json.load(f)
        except Exception as e:
            print(f"Error loading leagueTables.json: {e}")

    # ================= 1. DRIVERS CHAMPIONSHIP (TOP LEFT) =================
    driversBox = tk.LabelFrame(
        leaguesFrame,
        text=" 🏎️ F1 Drivers ",
        font=("Segoe UI", 9, "bold"),
        fg="#38bdf8",
        bg="#1e293b",
        bd=1,
        relief="solid",
    )
    driversBox.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=(10, 5))

    driversText = tk.Text(
        driversBox,
        bg="#1e293b",
        fg="white",
        font=("Consolas", 8),
        bd=0,
        wrap="word",
    )
    driversText.pack(fill="both", expand=True, padx=6, pady=6)

    drivers = leagueTables.get("Drivers Standings", [])
    if not drivers:
        driversText.insert("end", "No driver data.\n")
    else:
        for d in drivers:
            pos = str(d.get("position", "-")).rjust(2)
            d_info = d.get("Driver", {})
            name = (
                f"{d_info.get('givenName', '')} {d_info.get('familyName', '')}".strip()
            )
            pts = str(d.get("points", "0")).rjust(3)
            driversText.insert("end", f"{pos}. {name:<18} {pts}p\n")

    # ================= 2. CONSTRUCTORS CHAMPIONSHIP (TOP RIGHT) =================
    constructorsBox = tk.LabelFrame(
        leaguesFrame,
        text=" 🏎️ F1 Constructors ",
        font=("Segoe UI", 9, "bold"),
        fg="#38bdf8",
        bg="#1e293b",
        bd=1,
        relief="solid",
    )
    constructorsBox.grid(
        row=0, column=1, sticky="nsew", padx=(5, 10), pady=(10, 5)
    )

    constructorsText = tk.Text(
        constructorsBox,
        bg="#1e293b",
        fg="white",
        font=("Consolas", 8),
        bd=0,
        wrap="word",
    )
    constructorsText.pack(fill="both", expand=True, padx=6, pady=6)

    constructors = leagueTables.get("Constructors Standings", [])
    if not constructors:
        constructorsText.insert("end", "No constructor data.\n")
    else:
        for c in constructors:
            pos = str(c.get("position", "-")).rjust(2)
            c_info = c.get("Constructor", {})
            team = c_info.get("name", "Unknown")
            pts = str(c.get("points", "0")).rjust(3)
            constructorsText.insert("end", f"{pos}. {team:<16} {pts}p\n")

    # ================= 3. RUGBY PREMIERSHIP (BOTTOM FULL WIDTH) =================
    rugbyBox = tk.LabelFrame(
        leaguesFrame,
        text=" 🏉 Rugby Premiership ",
        font=("Segoe UI", 9, "bold"),
        fg="#38bdf8",
        bg="#1e293b",
        bd=1,
        relief="solid",
    )
    # columnspan=2 makes it stretch across both columns
    rugbyBox.grid(
        row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(5, 10)
    )

    rugbyText = tk.Text(
        rugbyBox,
        bg="#1e293b",
        fg="white",
        font=("Consolas", 8),
        bd=0,
        wrap="word",
    )
    rugbyText.pack(fill="both", expand=True, padx=8, pady=6)

    rugby_list = leagueTables.get("Prem Rugby Standings", [])
    if not rugby_list:
        rugbyText.insert("end", "No rugby standings data available.\n")
    else:
        for r in rugby_list:
            pos = str(
                r.get("position") or r.get("pos") or r.get("intRank") or "-"
            ).rjust(2)
            team = (
                r.get("name")
                or r.get("team")
                or r.get("strTeam")
                or "Unknown Team"
            )
            played = r.get("played") or r.get("intPlayed") or "-"
            pts = r.get("points") or r.get("pts") or r.get("intPoints") or "-"
            rugbyText.insert(
                "end", f"{pos}. {team:<20} | P: {played:<2} Pts: {pts}\n"
            )
    

def homeTab(notebook):
    # --- Matches Tab Container ---
    matchesFrame = tk.Frame(notebook, bg="#1e293b")
    notebook.add(matchesFrame, text="Matches")

    # Force exact 50/50 vertical division between row 0 and row 1
    matchesFrame.rowconfigure(0, weight=1)
    matchesFrame.columnconfigure(0, weight=1, uniform="matches_col")
    matchesFrame.columnconfigure(1, weight=1, uniform="matches_col")

    # Load match data safely
    matches_data = {}
    matches_file = JSONS_DIR / "matches.json"
    if matches_file.exists():
        try:
            with open(matches_file, "r", encoding="utf-8") as f:
                matches_data = json.load(f)
        except Exception as e:
            print(f"Error loading matches.json: {e}")

    # ================= 1. UPCOMING MATCHES (TOP HALF - 50%) =================
    upcomingBox = tk.LabelFrame(
        matchesFrame,
        text=" Upcoming Matches ",
        font=("Segoe UI", 9, "bold"),
        fg="#38bdf8",
        bg="#1e293b",
        bd=1,
        relief="solid",
    )
    upcomingBox.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

    upcomingMatchesText = tk.Text(
        upcomingBox,
        bg="#1e293b",
        fg="white",
        font=("Consolas", 8),
        bd=0,
        wrap="word",
    )
    upcomingMatchesText.pack(fill="both", expand=True, padx=8, pady=6)

    upcoming_list = matches_data.get("Upcoming Matches", [])
    if not upcoming_list:
        upcomingMatchesText.insert("end", "No upcoming fixtures scheduled.\n")
    else:
        for match in upcoming_list:
            date = match.get("dateEvent", "")
            time_str = match.get("strTime", "")
            league = match.get("strLeague", "")
            hTeam = match.get("strHomeTeam", "")
            aTeam = match.get("strAwayTeam", "")
            time_display = f" | {time_str[:5]}" if time_str else ""

            upcomingMatchesText.insert(
                "end",
                f"{date}{time_display} | {league}\n  {hTeam} vs {aTeam}\n\n",
            )

    # ================= 2. RECENT RESULTS (BOTTOM HALF - 50%) =================
    recentBox = tk.LabelFrame(
        matchesFrame,
        text=" Recent Results ",
        font=("Segoe UI", 9, "bold"),
        fg="#38bdf8",
        bg="#1e293b",
        bd=1,
        relief="solid",
    )
    recentBox.grid(row=0, column=1, sticky="nsew", padx=10, pady=(5, 10))

    recentMatchesText = tk.Text(
        recentBox,
        bg="#1e293b",
        fg="white",
        font=("Consolas", 8),
        bd=0,
        wrap="word",
    )
    recentMatchesText.pack(fill="both", expand=True, padx=8, pady=6)

    recent_list = matches_data.get("Recent Matches", [])
    if not recent_list:
        recentMatchesText.insert("end", "No recent match records found.\n")
    else:
        for match in recent_list:
            date = match.get("dateEvent", "")
            league = match.get("strLeague", "")
            hTeam = match.get("strHomeTeam", "")
            aTeam = match.get("strAwayTeam", "")
            hScore = match.get("intHomeScore", "-")
            aScore = match.get("intAwayScore", "-")

            recentMatchesText.insert(
                "end",
                f"{date} | {league}\n  {hTeam} {hScore} - {aScore} {aTeam}\n\n",
            )

def build_gui():
    """Reads the JSON files and renders a desktop/mobile-friendly UI window."""
    root = tk.Tk()
    root.title("Sports Hub")
    root.geometry("450x650")
    root.configure(bg="#0f172a")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    #-- Tabs --
    homeTab(notebook)
    matchesTab(notebook)
    leaguesTab(notebook)

    root.mainloop()


if __name__ == "__main__":
    # 1. Execute updaters to refresh JSON files (uncomment when needed)
    run_all_updates()

    # 2. Read JSONs and open display window
    build_gui()

    #Next to add is the highlight 
    # videos for each match, 
    # add f1 races to upcoming matches,
    # add individual athletes such as athletics and tennis
    