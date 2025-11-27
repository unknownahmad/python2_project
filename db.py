import sqlite3
import os

DB_PATH = "data/users.db"        # Path to the main user database.
TEST_DB_PATH = "data/test_users.db"  # Path to the test database.


def get_connection(test=False):
    """Returns a database connection, using the test database if test=True."""
    os.makedirs("data", exist_ok=True)
    path = TEST_DB_PATH if test else DB_PATH
    return sqlite3.connect(path)


def init_db(test=False):
    """Creates the users table if it does not already exist."""
    conn = get_connection(test=test)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            age INTEGER NOT NULL,
            age_verified INTEGER DEFAULT 0,
            total_winnings REAL DEFAULT 0,
            tournaments_won INTEGER DEFAULT 0,
            tournaments_lost INTEGER DEFAULT 0,
            games_played INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
