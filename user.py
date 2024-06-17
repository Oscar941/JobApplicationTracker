import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH')


class DBConnection:
    _conn = None

    @staticmethod
    def get_instance():
        if DBConnection._conn is None:
            DBConnection._conn = sqlite3.connect(DATABASE_PATH)
            DBConnection._conn.execute("PRAGMA foreign_keys = ON")
        return DBConnection._conn


def execute_query(query, params=None, commit=False, fetchone=False):
    conn = DBConnection.get_instance()
    cursor = conn.cursor()

    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)

    if commit:
        conn.commit()

    if fetchone:
        return cursor.fetchone()
    return cursor.fetchall()


def add_user(username, email, hashed_password):
    try:
        query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
        execute_query(query=query, params=(username, email, hashed_password), commit=True)
    except sqlite3.Error as error:
        print(f"Failed to add user {username}, error: {str(error)}")


def get_user_by_username(username):
    try:
        user_data = execute_query("SELECT * FROM users WHERE username = ?", (username,), fetchone=True)
        return user_data
    except sqlite3.Error as error:
        print(f"Failed to retrieve user {username}, error: {str(error)}")
        return None


def update_user_details(username, email=None, password=None):
    try:
        query, attributes = "UPDATE users SET ", []
        if email:
            query += "email = ?, "
            attributes.append(email)
        if password:
            query += "password = ?, "
            attributes.append(password)
        query = query.rstrip(", ")
        query += " WHERE username = ?"
        attributes.append(username)

        execute_query(query=query, params=tuple(attributes), commit=True)
    except sqlite3.Error as error:
        print(f"Failed to update user details for {username}, error: {str(error)}")


def close_db_connection():
    if DBConnection._conn:
        DBConnection._conn.close()