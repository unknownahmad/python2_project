import sqlite3
import re
from db import get_connection
from user import User, PremiumUser
from logger import log


# ============================
# DECORATOR: log function call
# ============================
def log_call(func):
    # Logs the function name every time the function is called.
    def wrapper(*args, **kwargs):
        log(f"[DECORATOR] Called function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


# ============================
# Check if password is valid
# ============================
def valid_password(password):
    # Checks if the password is at least 8 characters and contains letters and numbers.
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
    return bool(re.match(pattern, password))


# ============================
# register user
# ============================
@log_call
def register_user(username, password, age, test=False):
    # Registers a new user and stores their data in the database.
    if not valid_password(password):
        return "weak_password"

    conn = get_connection(test=test)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users(username, password, age, age_verified)
            VALUES (?, ?, ?, ?)
        """, (username, password, age, 1 if age >= 21 else 0))
        conn.commit()
        log(f"User registered: {username}")
        return "success"
    except sqlite3.IntegrityError:
        # Returns an error if the username already exists.
        return "username_taken"
    finally:
        conn.close()


# ============================
# Log in
# ============================
@log_call
def authenticate(username, password, test=False):
    # Authenticates a user and returns a User or PremiumUser object.
    conn = get_connection(test=test)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, password, age, age_verified, total_winnings,
               tournaments_won, tournaments_lost, games_played
        FROM users WHERE username=?
    """, (username,))
    data = cursor.fetchone()
    conn.close()

    if not data:
        return None

    db_user, db_pass, age, age_verified, winnings, wins, losses, games = data

    if db_pass != password:
        return None

    if winnings is None:
        winnings = 0

    if winnings >= 10000:
        # Returns a PremiumUser if winnings are 10k or more.
        return PremiumUser(db_user, age, age_verified, winnings, wins, losses, games)

    # Returns a normal User otherwise.
    return User(db_user, age, age_verified, winnings, wins, losses, games)


# ============================
# Update after loss
# ============================
@log_call
def update_after_loss(username, test=False):
    # Increments the user's loss count and games played.
    conn = get_connection(test=test)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET tournaments_lost = tournaments_lost + 1,
            games_played = games_played + 1
        WHERE username=?
    """, (username,))
    conn.commit()
    conn.close()


# ============================
# Update after win
# ============================
@log_call
def update_after_win(username, amount, test=False):
    # Increments win count, adds winnings, and increases games played.
    conn = get_connection(test=test)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET tournaments_won = tournaments_won + 1,
            total_winnings = total_winnings + ?,
            games_played = games_played + 1
        WHERE username=?
    """, (amount, username))
    conn.commit()
    conn.close()


# ============================
# Update after cashout
# ============================
@log_call
def update_after_cashout(username, amount, test=False):
    # Adds cashout amount to total winnings and increases games played.
    conn = get_connection(test=test)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET total_winnings = total_winnings + ?,
            games_played = games_played + 1
        WHERE username=?
    """, (amount, username))
    conn.commit()
    conn.close()
