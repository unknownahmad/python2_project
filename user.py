class User:
    def __init__(self, username, age, age_verified, winnings, wins, losses, games):
        self.username = username
        self.age = age
        self.age_verified = age_verified
        self.total_winnings = winnings
        self.tournaments_won = wins
        self.tournaments_lost = losses
        self.games_played = games
