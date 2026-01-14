import sqlite3
import hashlib

DB_NAME = "users.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        tier TEXT DEFAULT 'FREE'
    )
    """)

    # Admin account
    c.execute("SELECT * FROM users WHERE email = ?", ("admin@local",))
    if not c.fetchone():
        c.execute(
            "INSERT INTO users (email, password, tier) VALUES (?, ?, ?)",
            ("admin@local", hash_password("admin123"), "ADMIN")
        )

    conn.commit()
    conn.close()


def register_user(email, password):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, hash_password(password))
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "SELECT tier FROM users WHERE email = ? AND password = ?",
        (email, hash_password(password))
    )

    user = c.fetchone()
    conn.close()
    return user
