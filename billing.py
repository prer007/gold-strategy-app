import sqlite3

DB = "users.db"

def upgrade_user(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "UPDATE users SET tier = 'PRO' WHERE username = ?",
        (username,)
    )
    conn.commit()
    conn.close()
