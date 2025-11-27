import sqlite3
import re
from db import get_connection
from user import User
from logger import log

def valid_password(password):
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
    return bool(re.match(pattern, password))

def register_user(username, password, age, test=False):
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
        return "username_taken"
    finally:
        conn.close()

def authenticate(username, password, test=False):
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

    return User(db_user, age, age_verified, winnings, wins, losses, games)

def update_after_loss(username, test=False):
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

def update_after_win(username, amount, test=False):
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

def update_after_cashout(username, amount, test=False):
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
