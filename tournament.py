import random
import time

from betting import get_user_team, get_bet_amount
from utils import clear_screen, load_teams
from logger import log
from auth import update_after_win, update_after_loss, update_after_cashout

MULTIPLIERS = {
    "Round of 16": 1.2,
    "Quarter Finals": 1.5,
    "Semi Finals": 1.8,
    "Final": 2.5
}

def simulate_match(user_team, opponent):
    print(f"\nMatch: {user_team} vs {opponent}")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="")
    print()

    score1 = random.randint(0, 3)
    score2 = random.randint(0, 3)
    print(f"Final Score: {user_team} {score1} - {score2} {opponent}")

    if score1 > score2:
        return True
    if score1 < score2:
        return False

    time.sleep(1)
    pen1 = random.randint(3, 5)
    pen2 = random.randint(3, 5)

    while pen1 == pen2:
        pen1 += random.randint(0, 1)
        pen2 += random.randint(0, 1)

    print(f"Penalty: {pen1} - {pen2}")
    return pen1 > pen2

def get_opponent(user_team, available):
    return random.choice([t for t in available if t != user_team])

def play_tournament(user):
    clear_screen()
    print("Welcome to the Tournament!\n")

    if not user.age_verified:
        if user.age < 21:
            print("Access denied.")
            return

    team = get_user_team()
    bet = get_bet_amount()

    rounds = ["Round of 16", "Quarter Finals", "Semi Finals", "Final"]
    winnings = bet
    available = load_teams()

    for r in rounds:
        clear_screen()
        print("\n" + r)

        opp = get_opponent(team, available)
        available.remove(opp)

        win = simulate_match(team, opp)

        user.games_played += 1

        if not win:
            print(f"\nYou lost your bet of ${bet:.2f}")
            user.tournaments_lost += 1
            update_after_loss(user.username)
            return

        multiplier = MULTIPLIERS[r]
        winnings *= multiplier
        print(f"Current winnings: ${winnings:.2f}")

        if r == "Final":
            print("\nYou won the Champions League!")
            user.total_winnings += winnings
            user.tournaments_won += 1
            update_after_win(user.username, winnings)
            return

        while True:
            print("\n1. Continue")
            print("2. Cash Out")
            choice = input("> ").strip()

            if choice == "1":
                break

            if choice == "2":
                print(f"You cashed out: ${winnings:.2f}")
                user.total_winnings += winnings
                update_after_cashout(user.username, winnings)
                return
