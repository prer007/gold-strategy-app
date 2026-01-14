import sqlite3

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        tier TEXT DEFAULT 'FREE'
    )
    """)

    # Ensure admin user exists
    cur.execute("""
    INSERT OR IGNORE INTO users (username, tier)
    VALUES ('Justin', 'ADMIN')
    """)

    conn.commit()
    conn.close()
