from utils import load_teams

def check_age():
    while True:
        try:
            age = int(input("Enter your age: "))
            if age >= 21:
                return True
            else:
                print("You must be 21 or older to play.")
                return False
        except:
            print("Enter a valid number for age.")

def get_user_team():
    teams = load_teams()
    while True:
        print("Available teams:")
        for index in range(len(teams)):
            print(f"{index + 1}. {teams[index]}")
        choice = input("\nEnter team number or name: ").strip()
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(teams):
                return teams[num - 1]
            print("Invalid number.")
        else:
            for t in teams:
                if choice.lower() == t.lower():
                    return t
            print("Team not found.")

def get_bet_amount():
    while True:
        try:
            amt = float(input("\nEnter your bet amount: $"))
            if amt > 0:
                return amt
            print("Enter a positive number.")
        except:
            print("Invalid input. Enter a number.")
