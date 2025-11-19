import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading

from utils import load_teams, save_user_data, log_result
import random

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
        self.root.geometry("700x600")

        self.teams = load_teams()

        self.team_label = tk.Label(root, text="Choose your team:")
        self.team_label.pack(pady=5)

        self.team_var = tk.StringVar()
        self.team_dropdown = ttk.Combobox(
            root, textvariable=self.team_var,
            values=self.teams, state="readonly"
        )
        self.team_dropdown.pack(pady=5)

        self.bet_label = tk.Label(root, text="Enter bet amount:")
        self.bet_label.pack(pady=5)

        self.bet_entry = tk.Entry(root)
        self.bet_entry.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Tournament", command=self.start_game)
        self.start_button.pack(pady=10)

        self.output_box = tk.Text(root, height=20, width=80, state="disabled")
        self.output_box.pack(pady=10)

        self.cashout_button = tk.Button(root, text="Cash Out", command=self.cash_out)
        self.cashout_button.config(state="disabled")
        self.cashout_button.pack_forget()

        self.continue_button = tk.Button(root, text="Continue", command=self.continue_round)
        self.continue_button.config(state="disabled")
        self.continue_button.pack_forget()

        self.user_team = None
        self.bet_amount = 0
        self.winnings = 0
        self.available_teams = []
        self.current_round_index = 0
        self.rounds = ["Round of 16", "Quarter Finals", "Semi Finals", "Final"]
        self.game_running = False


    def write_output(self, text):
        self.output_box.config(state="normal")
        self.output_box.insert(tk.END, text + "\n")
        self.output_box.see(tk.END)
        self.output_box.config(state="disabled")


    def start_game(self):
        team = self.team_var.get()
        bet = self.bet_entry.get()

        self.cashout_button.pack_forget()
        self.cashout_button.config(state="disabled")

        self.continue_button.pack_forget()
        self.continue_button.config(state="disabled")

        if not team:
            messagebox.showerror("Error", "Select a team.")
            return

        try:
            bet = float(bet)
            if bet <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Enter a valid positive number for bet.")
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
        self.write_output("Team selected: " + team)
        self.write_output("Bet amount: $" + str(bet))
        self.write_output("----------------------------------------")

        threading.Thread(target=self.run_tournament).start()


    def get_opponent(self):
        choices = [t for t in self.available_teams if t != self.user_team]
        return random.choice(choices)

    def simulate_match(self, opponent):
        user_score = random.randint(0, 3)
        opp_score = random.randint(0, 3)

        self.write_output("Match: " + self.user_team + " vs " + opponent)
        self.write_output("Final Score: {} {} - {} {}".format(
            self.user_team, user_score, opp_score, opponent
        ))

        if user_score > opp_score:
            self.write_output("You win and advance.")
            return True, user_score, opp_score

        elif user_score < opp_score:
            self.write_output("You lose and are eliminated.")
            return False, user_score, opp_score

        else:
            self.write_output("Draw. Deciding winner...")
            time.sleep(1)
            win = random.choice([True, False])
            if win:
                self.write_output("You win after tiebreak.")
            else:
                self.write_output("You lose after tiebreak.")
            return win, user_score, opp_score


    def run_tournament(self):
        while self.current_round_index < len(self.rounds):

            if not self.game_running:
                return

            round_name = self.rounds[self.current_round_index]
            self.write_output("")
            self.write_output("=== " + round_name + " ===")

            opponent = self.get_opponent()
            self.available_teams.remove(opponent)

            win, us, them = self.simulate_match(opponent)
            log_result(self.user_team, opponent, us, them, win, round_name)

            if not win:
                self.write_output("\nYou lost your full bet of $" + str(self.bet_amount))
                save_user_data(self.user_team, self.bet_amount, 0, False)

                self.cashout_button.pack_forget()
                self.cashout_button.config(state="disabled")

                self.continue_button.pack_forget()
                self.continue_button.config(state="disabled")

                self.game_running = False
                return

            multiplier = MULTIPLIERS[round_name]
            self.winnings *= multiplier
            self.write_output("Current winnings: ${:.2f}".format(self.winnings))

            if round_name == "Final":
                self.write_output("\nYour team won the Champions League.")
                self.write_output("Final winnings: ${:.2f}".format(self.winnings))
                save_user_data(self.user_team, self.bet_amount, self.winnings, True)

                self.cashout_button.pack_forget()
                self.cashout_button.config(state="disabled")

                self.continue_button.pack_forget()
                self.continue_button.config(state="disabled")

                self.game_running = False
                return

            self.cashout_button.config(state="normal")
            self.cashout_button.pack()

            self.continue_button.config(state="normal")
            self.continue_button.pack()

            self.write_output("\nChoose an option: Continue or Cash Out...\n")

            return  

    def continue_round(self):
        self.cashout_button.pack_forget()
        self.cashout_button.config(state="disabled")

        self.continue_button.pack_forget()
        self.continue_button.config(state="disabled")

        self.current_round_index += 1

        threading.Thread(target=self.run_tournament).start()

    def cash_out(self):
        if not self.game_running:
            return

        self.write_output("\nYou cashed out with ${:.2f}".format(self.winnings))
        save_user_data(self.user_team, self.bet_amount, self.winnings, True)

        self.cashout_button.pack_forget()
        self.cashout_button.config(state="disabled")

        self.continue_button.pack_forget()
        self.continue_button.config(state="disabled")

        self.current_round_index += 1
        threading.Thread(target=self.run_tournament).start()



def main():
    root = tk.Tk()
    app = CLGuiApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
