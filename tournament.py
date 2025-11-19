import random
import time

from betting import get_user_team, get_bet_amount
from utils import clear_screen, save_user_data, log_result, load_teams

MULTIPLIERS = {
    "Round of 16": 1.2,
    "Quarter Finals": 1.5,
    "Semi Finals": 1.8,
    "Final": 2.5
}

def simulate_match(user_team, opponent):
    print(f"\nMatch: {user_team} vs {opponent}")
    print("Simulating match", end="")

    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()

    user_score = random.randint(0, 3)
    opp_score = random.randint(0, 3)

    print(f"Final Score: {user_team} {user_score} - {opp_score} {opponent}")

    if user_score > opp_score:
        print("You win and advance.")
        return True, user_score, opp_score
    elif user_score < opp_score:
        print("You lose and are eliminated.")
        return False, user_score, opp_score
    else:
        print("Draw. Deciding the winner...")
        time.sleep(1)

        win = random.choice([True, False])
        if win:
            print("You win after tiebreak.")
        else:
            print("You lose after tiebreak.")
        return win, user_score, opp_score

def get_opponent(user_team, available):
    choices = [t for t in available if t != user_team]
    return random.choice(choices)

def play_tournament():
    clear_screen()
    user_team = get_user_team()
    bet = get_bet_amount()

    print(f"\nYou selected: {user_team}")
    print(f"Bet placed: ${bet:.2f}")
    input("\nPress Enter to begin...")

    available_teams = load_teams()
    winnings = bet
    rounds = ["Round of 16", "Quarter Finals", "Semi Finals", "Final"]

    for round_name in rounds:
        clear_screen()
        print(f"\n{round_name}")
        print("----------------------------------------")

        opponent = get_opponent(user_team, available_teams)
        available_teams.remove(opponent)

        win, us, them = simulate_match(user_team, opponent)
        log_result(user_team, opponent, us, them, win, round_name)

        if not win:
            print(f"\nYou lost your full bet of ${bet:.2f}.")
            save_user_data(user_team, bet, 0, False)
            return

        multiplier = MULTIPLIERS[round_name]
        winnings *= multiplier

        print(f"\nCurrent Winnings: ${winnings:.2f}  (Multiplier x{multiplier})")

        if round_name == "Final":
            print("\nCongratulations. Your team won the Champions League.")
            print(f"Final Winnings: ${winnings:.2f}")
            save_user_data(user_team, bet, winnings, True)
            return

        while True:
            print("\nOptions:")
            print("1. Continue")
            print("2. Cash out")

            choice = input("> ").strip()

            if choice == "1":
                break
            elif choice == "2":
                print(f"\nYou cashed out with ${winnings:.2f}")
                save_user_data(user_team, bet, winnings, True)
                return
            else:
                print("Invalid choice.")
