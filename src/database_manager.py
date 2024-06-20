import datetime
import os
import sqlite3
from tkinter import messagebox

import pygame

from config import SCREENSHOT_DIR, DATABASE_FILE


def create_database():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # Create users Table
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        email TEXT UNIQUE,
                        password_hash TEXT
                    )""")

    # Create screenshots Table
    c.execute("""CREATE TABLE IF NOT EXISTS screenshots (
                        screenshot_id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        timestamp TEXT,
                        screenshot_data BLOB,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )""")

    # Create tags Table
    c.execute("""CREATE TABLE IF NOT EXISTS tags (
                        tag_id INTEGER PRIMARY KEY,
                        tag_name TEXT UNIQUE
                    )""")

    # Create screenshot_tags Junction Table
    c.execute("""CREATE TABLE IF NOT EXISTS screenshot_tags (
                        screenshot_id INTEGER,
                        tag_id INTEGER,
                        PRIMARY KEY (screenshot_id, tag_id),
                        FOREIGN KEY (screenshot_id) REFERENCES screenshots(screenshot_id),
                        FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
                    )""")

    # Create comments Table
    c.execute("""CREATE TABLE IF NOT EXISTS comments (
                        comment_id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        screenshot_id INTEGER,
                        timestamp TEXT,
                        comment_text TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(user_id),
                        FOREIGN KEY (screenshot_id) REFERENCES screenshots(screenshot_id)
                    )""")

    conn.commit()

    c.close()
    conn.close()

def save_screenshot(user_id, tag):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{timestamp}.png")

    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    pygame.image.save(pygame.display.get_surface(), screenshot_path)

    # Save the screenshot to the database
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    with open(screenshot_path, 'rb') as f:
        screenshot_blob = f.read()

    c.execute(
        "INSERT INTO screenshots (user_id, timestamp, screenshot_data) VALUES (?, ?, ?)",
        (user_id, timestamp, sqlite3.Binary(screenshot_blob))
    )
    screenshot_id = c.lastrowid
    conn.commit()

    c.execute("SELECT tag_id FROM tags WHERE tag_name = ?", (tag,))
    tag_id_row = c.fetchone()
    tag_id = tag_id_row[0]

    c.execute(
            "INSERT INTO screenshot_tags (screenshot_id, tag_id) VALUES (?, ?)",
            (screenshot_id, tag_id)
    )
    conn.commit()

    c.close()
    conn.close()

    return screenshot_id


def add_tag(tag_name):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    try:
        c.execute("SELECT tag_name FROM tags WHERE tag_name=?", (tag_name,))
        existing_tag = c.fetchone()

        if existing_tag:
            messagebox.showerror("Error", "Tag already exists")
            return False

        c.execute("INSERT INTO tags (tag_name) VALUES (?)", (tag_name,))
        conn.commit()
    except sqlite3.Error as error:
        messagebox.showerror("Error", "Tag creation failed")
        return False
    finally:
        c.close()
        conn.close()

    return True


def upload_comment(comment_text, user_id, screenshot_id):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()

        current_timestamp = datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'
        )

        c.execute("""
            INSERT INTO comments (user_id, screenshot_id, timestamp, comment_text)
            VALUES (?, ?, ?, ?)
        """, (user_id, screenshot_id, current_timestamp, comment_text))

        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error while uploading comment")
    finally:
        c.close()
        conn.close()


def find_photo_by_id(photo_id):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()

        # Retrieve photo details, time taken, associated tag name, and comments with username based on photo_id
        c.execute("""
            SELECT screenshots.timestamp, tags.tag_name, screenshots.screenshot_data, users.username, comments.timestamp, comments.comment_text
            FROM screenshots
            JOIN screenshot_tags ON screenshots.screenshot_id = screenshot_tags.screenshot_id
            JOIN tags ON screenshot_tags.tag_id = tags.tag_id
            LEFT JOIN comments ON screenshots.screenshot_id = comments.screenshot_id
            LEFT JOIN users ON comments.user_id = users.user_id
            WHERE screenshots.screenshot_id = ?

        """, (photo_id,))
        results = c.fetchall()

        if results:
            time_taken, tag_name, screenshot_blob = results[0][:3]
            comments = [
                (
                    username,
                    comment_timestamp,
                    comment_text
                ) for _, _, _, username, comment_timestamp, comment_text in results if comment_text
            ]
            return screenshot_blob, time_taken, tag_name, comments
        else:
            # Handle the case where the photo with the given ID doesn't exist
            return None, None, None, None
    except sqlite3.Error as e:
        messagebox.showerror(
                "Error", "Error while retrieving photo details"
        )
        print(e)
        return None, None, None, None
    finally:
        c.close()
        conn.close()


def get_valid_screenshots(tag_option, user_option, start_date, end_date):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    query = "SELECT screenshots.screenshot_id, screenshots.user_id, users.username, screenshots.timestamp, tags.tag_id, tags.tag_name " \
            "FROM screenshots " \
            "INNER JOIN users ON screenshots.user_id = users.user_id " \
            "INNER JOIN screenshot_tags ON screenshot_tags.screenshot_id = screenshots.screenshot_id " \
            "INNER JOIN tags ON tags.tag_id = screenshot_tags.tag_id " \
            "WHERE 1=1"

    params = []

    if tag_option != "All":
        tag_id, tag_name = tag_option.split(": ")
        query += " AND tags.tag_id = ?"
        params.append(tag_id)

    if user_option != "All":
        user_id, username = user_option.split(": ")
        query += " AND users.user_id = ?"
        params.append(user_id)

    if start_date and end_date:
        start_date_formatted = start_date + "_00-00-00"
        end_date_formatted = end_date + "_23-59-59"
        query += " AND screenshots.timestamp BETWEEN ? AND ?"
        params.extend([start_date_formatted, end_date_formatted])

    c.execute(query, params)
    results = c.fetchall()

    c.close()
    conn.close()

    return results


def get_tags():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("SELECT tag_id, tag_name FROM tags")
    tags = c.fetchall()
    conn.close()
    return tags


def get_users():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, username FROM users")
    usernames = c.fetchall()
    conn.close()
    return usernames
