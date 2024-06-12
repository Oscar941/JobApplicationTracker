import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def add_user(username, email, hashed_password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
        conn.commit()
    except sqlite3.Error as error:
        print(f"Failed to add user {username}, error: {str(error)}")
    finally:
        if conn:
            conn.close()

def get_user_by_username(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        return user_data
    except sqlite3.Error as error:
        print(f"Failed to retrieve user {username}, error: {str(error)}")
        return None
    finally:
        if conn:
            conn.close()

def update_user_details(username, email=None, password=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query, attributes = "UPDATE users SET ", []
        if email:
            query += "email = ?, "
            attributes.append(email)
        if password:
            query += "password = ?, "
            attributes.append(password)
        query = query.strip(", ")
        query += " WHERE username = ?"
        attributes.append(username)
        cursor.execute(query, tuple(attributes))
        conn.commit()
    except sqlite3.Error as error:
        print(f"Failed to update user details for {username}, error: {str(error)}")
    finally:
        if conn:
            conn.close()