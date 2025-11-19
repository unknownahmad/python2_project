import os
from datetime import datetime


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_welcome():
    print("==============================================")
    print("       CHAMPIONS LEAGUE SIMULATOR")
    print("==============================================")
    print()


def load_teams():
    """Loads teams from data/teams.txt"""
    os.makedirs("data", exist_ok=True)

    try:
        with open("data/teams.txt", "r") as f:
            teams = [line.strip() for line in f.readlines() if line.strip()]
            return teams
    except FileNotFoundError:
        print("Error: data/teams.txt not found!")
        return []


def save_user_data(team, bet, winnings, won):
    """Saves last game result to data/user.txt"""
    os.makedirs("data", exist_ok=True)

    result = "WIN" if won else "LOSS"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = (
        f"Team: {team}\n"
        f"Bet: {bet}\n"
        f"Final Winnings: {winnings}\n"
        f"Result: {result}\n"
        f"Timestamp: {timestamp}\n"
    )

    with open("data/user.txt", "w") as f:
        f.write(content)


def log_result(team, opponent, us, them, win, round_name):
    """Appends a match result to logs/results.txt"""
    os.makedirs("logs", exist_ok=True)

    result = "WIN" if win else "LOSS"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = (
        f"[{timestamp}] {round_name}: "
        f"{team} {us}-{them} {opponent} Result: {result}\n"
    )

    with open("logs/results.txt", "a") as f:
        f.write(log_entry)
