import os


def clear_screen():
    """Clears the terminal screen on Windows or Unix systems."""
    os.system("cls" if os.name == "nt" else "clear")


def display_welcome():
    """Displays the main welcome banner for the simulator."""
    print("==================================================")
    print("        CHAMPIONS LEAGUE GAMBLING SIMULATOR")
    print("==================================================")
    print()


def load_teams():
    """Loads the list of teams from the data/teams.txt file."""
    try:
        with open("data/teams.txt", "r") as f:
            return [t.strip() for t in f.readlines() if t.strip()]
    except FileNotFoundError:
        print("Error: data/teams.txt not found!")
        return []


def team_generator():
    """Yields teams one by one from the loaded team list."""
    teams = load_teams()
    for t in teams:
        yield t
