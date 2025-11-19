from menu import main_menu
from utils import clear_screen

def main():
    while True:
        clear_screen()
        if not main_menu():
            break

if __name__ == "__main__":
    main()
