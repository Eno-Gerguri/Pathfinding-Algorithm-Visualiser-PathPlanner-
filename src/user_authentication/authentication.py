import sqlite3
import hashlib

from config import DATABASE_FILE


def create_user(username, email, password):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username = ? OR email = ?",
        (username, email)
    )
    existing_user = c.fetchone()
    if existing_user:
        c.close()
        conn.close()
        return False

    hashed_password = hash_password(password)

    c.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, hashed_password)
    )
    conn.commit()
    conn.close()
    return True

def verify_login(username, password):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute(
        "SELECT user_id, password_hash FROM users WHERE username = ?",
        (username,)
    )
    user_data = c.fetchone()
    conn.close()

    if user_data:
        user_id, hashed_password = user_data
        if hashed_password == hash_password(password):
            return user_id

def hash_password(password):
    # Hash the password using SHA-256
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
