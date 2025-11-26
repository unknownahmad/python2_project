import random
import time

from betting import get_user_team, get_bet_amount, check_age
from utils import clear_screen, load_teams
from logger import log

MULTIPLIERS = {
    "Round of 16": 1.2,
    "Quarter Finals": 1.5,
    "Semi Finals": 1.8,
    "Final": 2.5
}

def simulate_match(user_team, opponent):
    log(f"Match started: {user_team} vs {opponent}")

    print(f"\nMatch: {user_team} vs {opponent}")
    print("Simulating match", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()

    user_score = random.randint(0, 3)
    opp_score = random.randint(0, 3)

    print(f"Final Score: {user_team} {user_score} - {opp_score} {opponent}")
    log(f"Score: {user_score}-{opp_score}")

    if user_score > opp_score:
        print("You win and advance.")
        log("Result: WIN")
        return True, user_score, opp_score

    if user_score < opp_score:
        print("You lose and are eliminated.")
        log("Result: LOSS")
        return False, user_score, opp_score

    print("Draw. Going to penalty shootout...")
    log("Penalty shootout started")

    time.sleep(1)

    user_pen = random.randint(3, 5)
    opp_pen = random.randint(3, 5)

    while user_pen == opp_pen:
        user_pen += random.randint(0, 1)
        opp_pen += random.randint(0, 1)

    print(f"Penalty Shootout Score: {user_team} {user_pen} - {opp_pen} {opponent}")
    log(f"Penalty result: {user_pen}-{opp_pen}")

    if user_pen > opp_pen:
        print("You win the penalty shootout.")
        log("Result: WIN (penalties)")
        return True, user_score, opp_score
    else:
        print("You lose the penalty shootout.")
        log("Result: LOSS (penalties)")
        return False, user_score, opp_score

def get_opponent(user_team, available):
    return random.choice([t for t in available if t != user_team])

def play_tournament():
    clear_screen()
    print("Welcome to the Tournament!\n")

    log("Tournament started")

    if not check_age():
        print("Access denied.")
        log("Age check failed. Tournament blocked.")
        return

    user_team = get_user_team()
    bet = get_bet_amount()

    log(f"Team selected: {user_team}")
    log(f"Bet placed: {bet}")

    print("\nYou selected:", user_team)
    print(f"Your bet: ${bet:.2f}")

    input("\nPress Enter to begin...")

    rounds = ["Round of 16", "Quarter Finals", "Semi Finals", "Final"]
    winnings = bet
    available = load_teams()

    for round_name in rounds:
        clear_screen()
        print("\n" + round_name)
        print("--------------------------------------")
        log(f"Round started: {round_name}")

        opponent = get_opponent(user_team, available)
        available.remove(opponent)

        win, us, them = simulate_match(user_team, opponent)

        if not win:
            print(f"\nGame Over! You lost your bet of ${bet:.2f}")
            log(f"Eliminated in {round_name}. Lost {bet}")
            return

        multiplier = MULTIPLIERS[round_name]
        winnings *= multiplier

        print(f"\nCurrent winnings: ${winnings:.2f} (x{multiplier})")
        log(f"Winnings updated: {winnings}")

        if round_name == "Final":
            print(f"\nCONGRATULATIONS! {user_team} wins the Champions League!")
            print(f"Total winnings: ${winnings:.2f}")
            log(f"Tournament WON. Final winnings: {winnings}")
            return

        while True:
            print("\n1. Continue to next round")
            print("2. Cash out")

            choice = input("Enter 1 or 2: ").strip()

            if choice == "1":
                log("User selected: Continue")
                break

            elif choice == "2":
                print(f"\nYou cashed out: ${winnings:.2f}")
                print(f"Profit: ${winnings - bet:.2f}")
                log(f"User cashed out: {winnings}, Profit: {winnings - bet}")
                return

            else:
                print("Invalid choice.")
                log(f"Invalid choice in tournament menu: '{choice}'")