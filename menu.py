import time
from utils import clear_screen, display_welcome
from tournament import play_tournament
from auth import authenticate, register_user
from logger import log

current_user = None


def login_menu():
    """Handles the login and registration menu for user authentication."""
    global current_user

    print("1. Login")
    print("2. Register")
    print("3. Back")

    choice = input("\nEnter choice: ").strip()

    if choice == "1":
        user = input("Username: ").strip()
        pwd = input("Password: ").strip()
        u = authenticate(user, pwd)
        if u:
            current_user = u
            log(f"User logged in: {u.username}")
            print("\nLogin successful.")
            time.sleep(1)
            return True
        else:
            print("Invalid login.")
            time.sleep(1)
            return True

    elif choice == "2":
        user = input("Choose username: ").strip()
        pwd = input("Choose password: ").strip()
        age = int(input("Enter age: ").strip())

        if register_user(user, pwd, age):
            print("\nRegistration successful.")
        else:
            print("\nUsername already taken.")
        time.sleep(1)
        return True

    else:
        return False


def main_menu():
    """Displays the main menu and handles navigation based on login state."""
    global current_user
    display_welcome()

    if current_user is None:
        print("1. Login/Register")
        print("2. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            login_menu()
            return True
        elif choice == "2":
            print("Goodbye.")
            return False
        else:
            return True

    print(f"Logged in as: {current_user.username}")
    print("1. Start New Game")
    print("2. Logout")
    print("3. Exit")

    choice = input("\nEnter choice: ").strip()

    if choice == "1":
        play_tournament(current_user)
        input("\nPress Enter to return...")
        return True

    elif choice == "2":
        current_user = None
        return True

    elif choice == "3":
        return False

    return True
