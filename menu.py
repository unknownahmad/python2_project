import time
from utils import clear_screen, display_welcome
from tournament import play_tournament

def main_menu():
    display_welcome()
    print("1. Start New Game")
    print("2. Exit")
    choice = input("\nEnter your choice (1-2): ").strip()
    if choice == "1":
        play_tournament()
        input("\nPress Enter to return to the menu...")
        return True
    elif choice == "2":
        print("\nThanks for playing. Goodbye.")
        time.sleep(1)
        return False
    else:
        print("Invalid choice. Enter 1 or 2.")
        time.sleep(1)
        return True
