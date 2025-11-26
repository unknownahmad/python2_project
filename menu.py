import time
from utils import clear_screen, display_welcome
from tournament import play_tournament
from logger import log

def main_menu():
    log("Menu opened")
    display_welcome()
    print("1. Start New Game")
    print("2. Exit")

    choice = input("\nEnter your choice (1-2): ").strip()

    if choice == "1":
        log("User selected: Start New Game")
        play_tournament()
        input("\nPress Enter to return to the menu...")
        return True

    elif choice == "2":
        log("User selected: Exit")
        print("\nThanks for playing. Goodbye.")
        time.sleep(1)
        return False

    else:
        log(f"Invalid menu choice: '{choice}'")
        print("Invalid choice. Enter 1 or 2.")
        time.sleep(1)
        return True