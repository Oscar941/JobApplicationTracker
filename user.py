import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH')

class DBConnection:
    """Singleton class to manage the database connection."""

    _conn = None

    @staticmethod
    def get_instance():
        """Get a singleton SQLite connection instance."""
        if DBConnection._conn is None:
            DBConnection._conn = sqlite3.connect(DATABASE_PATH)
            DBConnection._conn.execute("PRAGMA foreign_keys = ON")
        return DBConnection._conn

def execute_query(query, params=None, commit=False, fetchone=False):
    """Execute a SQL query with optional parameters, commit, and fetch modes."""
    conn = DBConnection.get_instance()
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    if commit:
        conn.commit()

    return cursor.fetchone() if fetchone else cursor.fetchall()

def add_user(username, email, hashed_password):
    """Add a new user with a username, email, and hashed password."""
    try:
        query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
        execute_query(query=query, params=(username, email, hashed_password), commit=True)
    except sqlite3.Error as error:
        print(f"Failed to add user {username}, error: {str(error)}")

def get_user_by_username(username):
    """Retrieve user data by username."""
    try:
        user_data = execute_query("SELECT * FROM users WHERE username = ?", (username,), fetchone=True)
        return user_data
    except sqlite3.Error as error:
        print(f"Failed to retrieve user {username}, error: {str(error)}")
        return None

def update_user_details(username, email=None, password=None):
    """Update a user's email and/or password by username."""
    try:
        updates = []
        values = []
        
        if email:
            updates.append("email = ?")
            values.append(email)
        if password:
            updates.append("password = ?")
            values.append(password)
        
        update_str = ", ".join(updates)
        query = f"UPDATE users SET {update_str} WHERE username = ?"
        values.append(username)

        execute_query(query=query, params=tuple(values), commit=True)
    except sqlite3.Error as error:
        print(f"Failed to update user details for {username}, error: {str(error)}")

def close_db_connection():
    """Close the database connection if it's open."""
    if DBConnection._conn:
        DBConnection._conn.close()