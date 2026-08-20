import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import getLeagues, getMatches

def run_all_updates():
    print("🔄 Updating JSON files...")
    getMatches.main()
    getLeagues.main()
    print("✅ JSON files updated.")


def load_json(filename):
    filepath = Path(filename)
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def build_gui():
    """Reads the JSON files and renders a desktop/mobile-friendly UI window."""
    root = tk.Tk()
    root.title("Sports Hub")
    root.geometry("450x650")
    root.configure(bg="#0f172a")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Recent Matches Tab ---
    recentMatchesFrame = tk.Frame(notebook, bg="#1e293b")
    notebook.add(recentMatchesFrame, text="Recent Matches")

    MatchesData = load_json("jsons/matches.json")  # Load your local JSON
    recentMatchesText = tk.Text(recentMatchesFrame, bg="#1e293b", fg="white", font=("Consolas", 10), bd=0)
    recentMatchesText.pack(fill="both", expand=True, padx=10, pady=10)
    for match in MatchesData.get("Recent Matches", []):
        date = match.get("dateEvent")
        hTeam = match.get("strHomeTeam")
        aTeam = match.get("strAwayTeam")
        hScore = match.get("intHomeScore")
        aScore = match.get("intAwayScore")
        league = match.get("strLeague")
        recentMatchesText.insert(
            "end", f"{date} | {league} | {hTeam} {hScore} - {aScore} {aTeam}\n"
        )

    for match in MatchesData.get("Upcoming Matches", []):
        date = match.get("dateEvent")
        hTeam = match.get("strHomeTeam")
        aTeam = match.get("strAwayTeam")
        hScore = match.get("intHomeScore")
        aScore = match.get("intAwayScore")
        league = match.get("strLeague")
        recentMatchesText.insert(
            "end", f"{date} | {league} | {hTeam} {hScore} - {aScore} {aTeam}\n"
        )

    # --- F1 Tab ---
    tablesFrame = tk.Frame(notebook, bg="#1e293b")
    notebook.add(tablesFrame, text="🏎️ F1")

    leagueTables = load_json("jsons/leagueTables.json")  # Load your local JSON
    f1_text = tk.Text(
        tablesFrame, bg="#1e293b", fg="white", font=("Consolas", 10), bd=0
    )
    f1_text.pack(fill="both", expand=True, padx=10, pady=10)
    for d in leagueTables.get("drivers", []):
        f1_text.insert(
            "end", f"{d.get('pos', '-')}. {d.get('name')} - {d.get('pts')} pts\n"
        )

    for c in leagueTables.get("constructors", []):
        f1_text.insert(
            "end",
            f"{c.get('pos', '-')}. {c.get('team')} - {c.get('pts')} pts\n",
        )

    # --- Rugby Tab ---
    rugby_frame = tk.Frame(notebook, bg="#1e293b")
    notebook.add(rugby_frame, text="🏉 Rugby")

    rugby_text = tk.Text(
        rugby_frame, bg="#1e293b", fg="white", font=("Consolas", 10), bd=0
    )
    rugby_text.pack(fill="both", expand=True, padx=10, pady=10)
    for r in leagueTables.get("rugby", []):
        rugby_text.insert(
            "end",
            f"{r.get('pos', '-')}. {r.get('team')} | P:{r.get('played')} Pts:{r.get('pts')}\n",
        )

    root.mainloop()


if __name__ == "__main__":

    build_gui()  # Launch the GUI window

    # 1. Execute updaters to refresh JSON files
    run_all_updates()

    # 2. Read JSONs and open display window
    build_gui()



