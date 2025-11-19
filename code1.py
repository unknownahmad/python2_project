import random
import time
import os


TEAMS = [
    "Real Madrid", "Barcelona", "Bayern Munich", "Manchester City",
    "PSG", "Liverpool", "Chelsea", "Juventus",
    "AC Milan", "Inter Milan", "Arsenal", "Dortmund",
    "Ajax", "Benfica", "Porto", "Atletico Madrid"
]


MULTIPLIERS = {
    "Round of 16": 1.2,
    "Quarter Finals": 1.5,
    "Semi Finals": 1.8,
    "Final": 2.5
}

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("    CHAMPIONS LEAGUE GAMBLING SIMULATOR")
    print("=" * 50)
    print()

def get_user_team():
    """Get user to select a team"""
    while True:
        print("Available teams:")
        for i, team in enumerate(TEAMS, 1):
            print(f"{i}. {team}")
        
        try:
            choice = input("\nEnter the number or name of your team: ").strip()
            
            
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(TEAMS):
                    return TEAMS[choice_num - 1]
                else:
                    print("❌ Invalid number! Please choose between 1-16")
            
            
            else:
                for team in TEAMS:
                    if choice.lower() == team.lower():
                        return team
                print("❌ Team not found! Please try again.")
                
        except ValueError:
            print("❌ Invalid input! Please enter a number or team name.")

def get_bet_amount():
    """Get bet amount from user"""
    while True:
        try:
            amount = float(input("\nEnter your bet amount: $"))
            if amount > 0:
                return amount
            else:
                print("❌ Please enter a positive amount!")
        except ValueError:
            print("❌ Invalid amount! Please enter a number.")

def simulate_match(user_team, opponent):
    """Simulate a match and return the result"""
    print(f"\n⚽ Match: {user_team} vs {opponent}")
    print("Simulating match", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()
    
    
    user_score = random.randint(0, 3)
    opponent_score = random.randint(0, 3)
    
    print(f"📊 Final Score: {user_team} {user_score} - {opponent_score} {opponent}")
    
    if user_score > opponent_score:
        print("🎉 YOU WIN! Your team advances!")
        return True, user_score, opponent_score
    elif user_score < opponent_score:
        print("💀 YOU LOSE! Your team is eliminated!")
        return False, user_score, opponent_score
    else:
        
        print("⚡ It's a draw! Going to penalty shootout...")
        time.sleep(1)
        penalty_win = random.choice([True, False])
        if penalty_win:
            print("🎉 YOU WIN THE PENALTIES! Your team advances!")
            return True, user_score, opponent_score
        else:
            print("💀 YOU LOSE THE PENALTIES! Your team is eliminated!")
            return False, user_score, opponent_score

def get_opponent(user_team, available_teams):
    """Get a random opponent from available teams"""
    opponents = [team for team in available_teams if team != user_team]
    return random.choice(opponents)

def play_tournament():
    """Main game function"""
    clear_screen()
    display_welcome()
    
    
    user_team = get_user_team()
    bet_amount = get_bet_amount()
    
    print(f"\n✅ You selected: {user_team}")
    print(f"💰 Your bet: ${bet_amount:.2f}")
    
    input("\nPress Enter to start the tournament...")
    
    
    rounds = ["Round of 16", "Quarter Finals", "Semi Finals", "Final"]
    current_amount = bet_amount
    available_teams = TEAMS.copy()
    
    for round_name in rounds:
        clear_screen()
        print(f"\n🏆 {round_name}")
        print("=" * 30)
        
        
        opponent = get_opponent(user_team, available_teams)
        available_teams.remove(opponent)
        
        
        win, user_score, opponent_score = simulate_match(user_team, opponent)
        
        if not win:
            print(f"\n💸 Game Over! You lost your bet of ${bet_amount:.2f}")
            return
        
        
        multiplier = MULTIPLIERS[round_name]
        current_amount *= multiplier
        
        print(f"\n💰 Current winnings: ${current_amount:.2f} (x{multiplier})")
        
        
        if round_name == "Final":
            print(f"\n🎊 CONGRATULATIONS! {user_team} WINS THE CHAMPIONS LEAGUE!")
            print(f"🏆 TOTAL WINNINGS: ${current_amount:.2f}")
            break
        
        
        while True:
            print("\nWhat would you like to do?")
            print("1. Continue to next round")
            print("2. Cash out")
            
            choice = input("Enter your choice (1-2): ").strip()
            
            if choice == "1":
                print("🚀 Continuing to next round...")
                time.sleep(1)
                break
            elif choice == "2":
                print(f"\n💰 You cashed out with: ${current_amount:.2f}")
                print(f"💵 Profit: ${current_amount - bet_amount:.2f}")
                return
            else:
                print("❌ Invalid choice! Please enter 1 or 2")

def main():
    """Main program loop"""
    while True:
        clear_screen()
        display_welcome()
        
        print("1. Start New Game")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ").strip()
        
        if choice == "1":
            play_tournament()
        elif choice == "2":
            print("\nThanks for playing! Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice! Please enter 1 or 2")
            time.sleep(1)
        
        if choice == "1":
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()