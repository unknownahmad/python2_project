import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_welcome():
    print("==================================================")
    print("        CHAMPIONS LEAGUE GAMBLING SIMULATOR")
    print("==================================================")
    print()

def load_teams():
    try:
        with open("data/teams.txt", "r") as f:
            return [t.strip() for t in f.readlines() if t.strip()]
    except FileNotFoundError:
        print("Error: data/teams.txt not found!")
        return []
