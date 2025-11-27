from menu import main_menu
from utils import clear_screen
from db import init_db


def main():
    """Initializes the database and runs the main menu loop."""
    init_db()
    while True:
        clear_screen()
        if not main_menu():
            break


if __name__ == "__main__":
    main()
