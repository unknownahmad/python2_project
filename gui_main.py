import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import random

from utils import load_teams

MULTIPLIERS = {
    "Round of 16": 1.2,
    "Quarter Finals": 1.5,
    "Semi Finals": 1.8,
    "Final": 2.5
}

class CLGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Champions League Simulator")
        self.root.geometry("750x620")

        self.teams = load_teams()

        self.team_label = tk.Label(root, text="Choose your team:")
        self.team_label.pack(pady=6)

        self.team_var = tk.StringVar()
        self.team_dropdown = ttk.Combobox(
            root, textvariable=self.team_var,
            values=self.teams, state="readonly", width=40
        )
        self.team_dropdown.pack(pady=4)

        self.bet_label = tk.Label(root, text="Enter bet amount:")
        self.bet_label.pack(pady=6)

        self.bet_entry = tk.Entry(root, width=20)
        self.bet_entry.pack(pady=4)

        self.start_button = tk.Button(root, text="Start Tournament", command=self.start_game)
        self.start_button.pack(pady=10)

        self.output_box = tk.Text(root, height=22, width=90, state="disabled", wrap="word")
        self.output_box.pack(pady=8)

        self.cashout_button = tk.Button(root, text="Cash Out", command=self.cash_out)
        self.cashout_button.config(state="disabled")
        self.cashout_button.pack_forget()

        self.continue_button = tk.Button(root, text="Continue", command=self.continue_round)
        self.continue_button.config(state="disabled")
        self.continue_button.pack_forget()

        self.user_team = None
        self.bet_amount = 0.0
        self.winnings = 0.0
        self.available_teams = []
        self.current_round_index = 0
        self.rounds = ["Round of 16", "Quarter Finals", "Semi Finals", "Final"]
        self.game_running = False

    def write_output(self, text):
        def _append():
            self.output_box.config(state="normal")
            self.output_box.insert(tk.END, text + "\n")
            self.output_box.see(tk.END)
            self.output_box.config(state="disabled")
        self.root.after(0, _append)

    def ask_age(self):
        age_ok = {"value": False} 
        dialog = tk.Toplevel(self.root)
        dialog.title("Age Verification")
        dialog.geometry("320x140")
        dialog.transient(self.root)
        dialog.grab_set() 

        tk.Label(dialog, text="Enter your age:").pack(pady=8)
        age_entry = tk.Entry(dialog, width=10)
        age_entry.pack(pady=4)

        def submit_age():
            val = age_entry.get().strip()
            try:
                age = int(val)
                if age >= 21:
                    age_ok["value"] = True
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "You must be 21 or older to play.")
                    age_ok["value"] = False
                    dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer for age.")

        submit_btn = tk.Button(dialog, text="Submit", command=submit_age)
        submit_btn.pack(pady=8)

        self.root.wait_window(dialog)
        return age_ok["value"]

    def start_game(self):
        self.cashout_button.pack_forget()
        self.cashout_button.config(state="disabled")
        self.continue_button.pack_forget()
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

        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.config(state="disabled")

        self.write_output("Tournament started.")
        self.write_output(f"Team selected: {team}")
        self.write_output(f"Bet amount: ${bet:.2f}")
        self.write_output("----------------------------------------")

        threading.Thread(target=self.run_tournament, daemon=True).start()

    def simulate_match(self, opponent):
        user_score = random.randint(0, 3)
        opp_score = random.randint(0, 3)

        self.write_output(f"Match: {self.user_team} vs {opponent}")
        self.write_output(f"Final Score: {self.user_team} {user_score} - {opp_score} {opponent}")

        if user_score > opp_score:
            self.write_output("You win and advance.")
            return True, user_score, opp_score
        elif user_score < opp_score:
            self.write_output("You lose and are eliminated.")
            return False, user_score, opp_score

        self.write_output("Match is a draw. Going to penalty shootout...")
        time.sleep(1)

        user_pen = random.randint(3, 5)
        opp_pen = random.randint(3, 5)

        while user_pen == opp_pen:
            user_pen += random.randint(0, 1)
            opp_pen += random.randint(0, 1)

        self.write_output(f"Penalty Shootout Score: {self.user_team} {user_pen} - {opp_pen} {opponent}")

        if user_pen > opp_pen:
            self.write_output("You win the penalty shootout.")
            return True, user_score, opp_score
        else:
            self.write_output("You lose the penalty shootout.")
            return False, user_score, opp_score

    def get_opponent(self):
        choices = [t for t in self.available_teams if t != self.user_team]
        return random.choice(choices)

    def run_tournament(self):
        while self.current_round_index < len(self.rounds):
            if not self.game_running:
                return

            round_name = self.rounds[self.current_round_index]
            self.write_output("")
            self.write_output(f"=== {round_name} ===")

            opponent = self.get_opponent()
            try:
                self.available_teams.remove(opponent)
            except ValueError:
                pass

            win, us, them = self.simulate_match(opponent)

            if not win:
                self.write_output(f"\nYou lost your full bet of ${self.bet_amount:.2f}")
                self.root.after(0, lambda: self.cashout_button.pack_forget())
                self.root.after(0, lambda: self.cashout_button.config(state="disabled"))
                self.root.after(0, lambda: self.continue_button.pack_forget())
                self.root.after(0, lambda: self.continue_button.config(state="disabled"))
                self.game_running = False
                return

            multiplier = MULTIPLIERS.get(round_name, 1)
            self.winnings *= multiplier
            self.write_output(f"Current winnings: ${self.winnings:.2f} (x{multiplier})")

            if round_name == "Final":
                self.write_output("\nYour team won the Champions League.")
                self.write_output(f"Final winnings: ${self.winnings:.2f}")
                self.root.after(0, lambda: self.cashout_button.pack_forget())
                self.root.after(0, lambda: self.cashout_button.config(state="disabled"))
                self.root.after(0, lambda: self.continue_button.pack_forget())
                self.root.after(0, lambda: self.continue_button.config(state="disabled"))
                self.game_running = False
                return

            self.root.after(0, lambda: self.cashout_button.config(state="normal"))
            self.root.after(0, lambda: self.cashout_button.pack())
            self.root.after(0, lambda: self.continue_button.config(state="normal"))
            self.root.after(0, lambda: self.continue_button.pack())

            self.write_output("\nChoose an option: Continue or Cash Out...\n")
            return

    def continue_round(self):
        self.cashout_button.pack_forget()
        self.cashout_button.config(state="disabled")
        self.continue_button.pack_forget()
        self.continue_button.config(state="disabled")

        self.current_round_index += 1

        threading.Thread(target=self.run_tournament, daemon=True).start()

    def cash_out(self):
        if not self.game_running:
            return

        self.cashout_button.pack_forget()
        self.cashout_button.config(state="disabled")
        self.continue_button.pack_forget()
        self.continue_button.config(state="disabled")

        self.write_output(f"\nYou cashed out with ${self.winnings:.2f}")

        self.current_round_index += 1
        threading.Thread(target=self.run_tournament, daemon=True).start()


def main():
    root = tk.Tk()
    app = CLGuiApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
