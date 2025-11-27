class User:
    """Represents a standard user with basic account and gameplay statistics."""
    
    def __init__(self, username, age, age_verified, winnings, wins, losses, games):
        self.username = username
        self.age = age
        self.age_verified = age_verified
        self.total_winnings = winnings
        self.tournaments_won = wins
        self.tournaments_lost = losses
        self.games_played = games

    @property
    def is_premium(self):
        """Indicates whether the user has premium status (always False for normal users)."""
        return False


class PremiumUser(User):
    """Represents a premium user with elevated privileges."""
    
    @property
    def is_premium(self):
        """Indicates that this user is premium."""
        return True
