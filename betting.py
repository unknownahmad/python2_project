from utils import load_teams

def get_user_team():
    teams = load_teams()

    while True:
        print("Available teams:")
        for i, t in enumerate(teams, 1):
            print(f"{i}. {t}")

        choice = input("\nEnter the number or name of your team: ").strip()

        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(teams):
                return teams[index - 1]
            else:
                print("Invalid number. Try again.")
        else:
            for team in teams:
                if team.lower() == choice.lower():
                    return team
            print("Team not found. Try again.")

def get_bet_amount():
    while True:
        try:
            amount = float(input("\nEnter bet amount: $"))
            if amount > 0:
                return amount
            print("Enter a positive number.")
        except ValueError:
            print("Invalid input. Enter a number.")
