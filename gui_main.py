import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import random
from db import init_db

from utils import load_teams, team_generator
from logger import log
from gui_login import LoginWindow
from auth import update_after_loss, update_after_win, update_after_cashout

MULTIPLIERS = {
    "Round of 16": 1.2,
    "Quarter Finals": 1.5,
    "Semi Finals": 1.8,
    "Final": 2.5
}

class CLGuiApp:
    def __init__(self, root, user):
        """Initializes the entire Champions League GUI app and prepares the interface."""
        self.root = root
        self.user = user
        print("User class:", type(self.user))
        self.root.title(f"Champions League Simulator - Logged in as {user.username}")
        self.root.geometry("750x750")
        self.root.configure(bg="#1b1f3b")

        log(f"GUI launched for user: {user.username}")

        self.teams = sorted(list(team_generator()), key=lambda t: t.lower())
        self.opponents_faced = set()

        # GUI setup...
        header = tk.Label(
            root,
            text="⚽ Champions League Tournament",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#1b1f3b"
        )
        header.pack(pady=10)

        if type(self.user).__name__ == "PremiumUser":
            premium_banner = tk.Label(
                root,
                text="💎 PREMIUM USER — VIP BENEFITS ACTIVE 💎",
                font=("Helvetica", 14, "bold"),
                fg="#f7d358",
                bg="#1b1f3b"
            )
            premium_banner.pack(pady=5)

        self.team_label = tk.Label(root, text="Choose your team:",
                                   font=("Helvetica", 12), fg="white", bg="#1b1f3b")
        self.team_label.pack(pady=6)

        self.team_var = tk.StringVar()
        self.team_dropdown = ttk.Combobox(root, textvariable=self.team_var,
                                          values=self.teams, state="readonly", width=40)
        self.team_dropdown.pack(pady=4)

        self.bet_label = tk.Label(root, text="Enter bet amount:",
                                  font=("Helvetica", 12), fg="white", bg="#1b1f3b")
        self.bet_label.pack(pady=6)

        self.bet_entry = tk.Entry(root, width=20, font=("Helvetica", 11))
        self.bet_entry.pack(pady=4)

        self.start_button = tk.Button(root, text="Start Tournament",
                                      command=self.start_game, width=20,
                                      bg="#4e73df", fg="white",
                                      font=("Helvetica", 12, "bold"),
                                      relief="raised", bd=3)
        self.start_button.pack(pady=10)

        self.output_box = tk.Text(
            root, height=22, width=90, wrap="word",
            state="disabled", bg="#f7f7f7",
            font=("Consolas", 10)
        )
        self.output_box.pack(pady=8)

        self.button_frame = tk.Frame(root, bg="#1b1f3b")
        self.button_frame.pack(pady=10)

        self.cashout_button = tk.Button(
            self.button_frame, text="Cash Out", width=15,
            bg="#ff6b6b", fg="white", font=("Helvetica", 11, "bold"),
            command=self.cash_out
        )
        self.cashout_button.grid(row=0, column=0, padx=6)
        self.cashout_button.config(state="disabled")

        self.continue_button = tk.Button(
            self.button_frame, text="Continue", width=15,
            bg="#38b000", fg="white", font=("Helvetica", 11, "bold"),
            command=self.continue_round
        )
        self.continue_button.grid(row=0, column=1, padx=6)
        self.continue_button.config(state="disabled")

        self.logout_button = tk.Button(
            self.button_frame, text="Logout", width=15,
            bg="#6c757d", fg="white", font=("Helvetica", 11, "bold"),
            command=self.logout
        )
        self.logout_button.grid(row=0, column=2, padx=6)

        # Game state
        self.user_team = None
        self.bet_amount = 0.0
        self.winnings = 0.0
        self.available_teams = []
        self.current_round_index = 0
        self.rounds = ["Round of 16", "Quarter Finals", "Semi Finals", "Final"]
        self.game_running = False

    def write_output(self, text):
        """Writes text to the output display box."""
        def _append():
            self.output_box.config(state="normal")
            self.output_box.insert(tk.END, text + "\n")
            self.output_box.see(tk.END)
            self.output_box.config(state="disabled")
        self.root.after(0, _append)

    def ask_age(self):
        """Prompts the user for age verification if they are not already verified."""
        if self.user.age_verified:
            return True

        age_ok = {"value": False}
        dialog = tk.Toplevel(self.root)
        dialog.title("Age Verification")
        dialog.geometry("320x140")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="#1b1f3b")

        tk.Label(dialog, text="Enter your age:", fg="white", bg="#1b1f3b",
                 font=("Helvetica", 12)).pack(pady=8)

        age_entry = tk.Entry(dialog, width=10, font=("Helvetica", 12))
        age_entry.pack(pady=4)

        def submit_age():
            val = age_entry.get().strip()
            try:
                age = int(val)
                if age >= 21:
                    age_ok["value"] = True
                    self.user.update_age_verified()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "You must be 21 or older to play.")
                    dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")

        tk.Button(dialog, text="Submit", command=submit_age,
                  bg="#4e73df", fg="white",
                  font=("Helvetica", 11, "bold")).pack(pady=8)

        self.root.wait_window(dialog)
        return age_ok["value"]

    def start_game(self):
        """Starts a new tournament, validating team selection and bet amount."""
        self.cashout_button.config(state="disabled")
        self.continue_button.config(state="disabled")

        if not self.ask_age():
            return

        team = self.team_var.get()
        bet_text = self.bet_entry.get().strip()

        if not team:
            messagebox.showerror("Error", "Select a team.")
            return

        try:
            bet = float(bet_text)
            if bet <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive bet amount.")
            return

        self.user_team = team
        self.bet_amount = bet
        self.winnings = bet
        self.available_teams = load_teams()
        self.current_round_index = 0
        self.game_running = True
        self.opponents_faced.clear()

        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.config(state="disabled")

        self.write_output("Tournament started.")
        self.write_output(f"Team selected: {team}")
        self.write_output(f"Bet amount: ${bet:.2f}")
        self.write_output("----------------------------------------")

        threading.Thread(target=self.run_tournament, daemon=True).start()

    def simulate_match(self, opponent):
        """Simulates a match against an opponent and determines the winner."""
        user_score = random.randint(0, 3)
        opp_score = random.randint(0, 3)

        self.write_output(f"Match: {self.user_team} vs {opponent}")
        self.write_output(f"Final Score: {self.user_team} {user_score} - {opp_score} {opponent}")

        if user_score > opp_score:
            return True, user_score, opp_score

        if user_score < opp_score:
            return False, user_score, opp_score

        time.sleep(1)
        self.write_output("Penalty Shootout...")

        user_pen = random.randint(3, 5)
        opp_pen = random.randint(3, 5)

        while user_pen == opp_pen:
            user_pen += random.randint(0, 1)
            opp_pen += random.randint(0, 1)

        self.write_output(f"Penalty Shootout Score: {user_pen} - {opp_pen}")

        return user_pen > opp_pen, user_score, opp_score

    def get_opponent(self):
        """Chooses a random opponent that is not the user's team."""
        choices = [t for t in self.available_teams if t != self.user_team]
        return random.choice(choices)

    def run_tournament(self):
        """Runs one tournament round at a time and handles progression or elimination."""
        while self.current_round_index < len(self.rounds):
            if not self.game_running:
                return

            round_name = self.rounds[self.current_round_index]
            self.write_output("")
            self.write_output(f"=== {round_name} ===")

            opponent = self.get_opponent()
            self.opponents_faced.add(opponent)

            if opponent in self.available_teams:
                self.available_teams.remove(opponent)

            win, us, them = self.simulate_match(opponent)

            if not win:
                self.write_output(f"\nYou lost your full bet of ${self.bet_amount:.2f}")
                update_after_loss(self.user.username)
                self.write_output(f"Opponents faced: {', '.join(self.opponents_faced)}")
                self.cashout_button.config(state="disabled")
                self.continue_button.config(state="disabled")
                self.game_running = False
                return

            multiplier = MULTIPLIERS.get(round_name, 1)
            self.winnings *= multiplier
            self.write_output(f"Current winnings: ${self.winnings:.2f} (x{multiplier})")

            if round_name == "Final":
                self.write_output("Your team won the Champions League!")
                self.write_output(f"Final winnings: ${self.winnings:.2f}")
                update_after_win(self.user.username, self.winnings)
                self.write_output(f"Opponents faced: {', '.join(self.opponents_faced)}")
                self.cashout_button.config(state="disabled")
                self.continue_button.config(state="disabled")
                self.game_running = False
                return

            self.cashout_button.config(state="normal")
            self.continue_button.config(state="normal")

            self.write_output("\nChoose an option: Continue or Cash Out...\n")
            return

    def continue_round(self):
        """Moves the tournament to the next round."""
        self.cashout_button.config(state="disabled")
        self.continue_button.config(state="disabled")
        self.current_round_index += 1
        threading.Thread(target=self.run_tournament, daemon=True).start()

    def cash_out(self):
        """Lets the user take their winnings and end the tournament early."""
        self.write_output(f"\nYou cashed out with ${self.winnings:.2f}")
        update_after_cashout(self.user.username, self.winnings)
        self.write_output(f"Opponents faced: {', '.join(self.opponents_faced)}")
        self.cashout_button.config(state="disabled")
        self.continue_button.config(state="disabled")
        self.game_running = False
        self.write_output("\nTournament ended — you cashed out.\n")

    def logout(self):
        """Logs the user out and returns to the login screen."""
        self.game_running = False
        self.root.destroy()

        new_root = tk.Tk()
        login = LoginWindow(new_root)
        new_root.mainloop()

        if login.user is None:
            return

        main_root = tk.Tk()
        app = CLGuiApp(main_root, login.user)
        main_root.mainloop()


def main():
    """Entry point — launches login window and then the main GUI when logged in."""
    root = tk.Tk()
    login = LoginWindow(root)
    root.mainloop()

    if login.user:
        new_root = tk.Tk()
        CLGuiApp(new_root, login.user)
        new_root.mainloop()


if __name__ == "__main__":
    main()
