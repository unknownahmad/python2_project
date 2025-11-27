from utils import load_teams
from logger import log


def check_age():
    """Asks the user for their age and returns True only if they are 21 or older."""
    while True:
        val = input("Enter your age: ").strip()
        try:
            age = int(val)
            if age >= 21:
                log(f"Age verified: {age}")
                return True
            else:
                print("You must be 21 or older to play.")
                log(f"Age check failed: entered {age}")
                return False
        except ValueError:
            print("Enter a valid number for age.")
            log(f"Invalid age input: '{val}'")


def get_user_team():
    """Lets the user choose a team by number or name and returns the selected team."""
    teams = load_teams()
    while True:
        print("Available teams:")
        for index, team in enumerate(teams, start=1):
            print(f"{index}. {team}")

        choice = input("\nEnter team number or name: ").strip()

        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(teams):
                team = teams[num - 1]
                log(f"Team selected by number: {team}")
                return team
            print("Invalid number.")
            log(f"Invalid team number: {choice}")
        else:
            for t in teams:
                if choice.lower() == t.lower():
                    log(f"Team selected by name: {t}")
                    return t
            print("Team not found.")
            log(f"Team not found input: '{choice}'")


def get_bet_amount():
    """Prompts the user for a bet amount and returns it as a positive number."""
    while True:
        val = input("\nEnter your bet amount: $").strip()
        try:
            amt = float(val)
            if amt > 0:
                log(f"Bet amount entered: {amt}")
                return amt
            print("Enter a positive number.")
            log(f"Invalid bet (not positive): {amt}")
        except ValueError:
            print("Invalid input. Enter a number.")
            log(f"Invalid bet input: '{val}'")
