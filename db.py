import sqlite3
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONNECTION_STRING = getenv('DATABASE_URL')

DATABASE_SCHEMA = """
CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS application(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    company_name TEXT NOT NULL,
    position TEXT NOT NOT NULL,
    status TEXT NOT NULL,
    application_date DATE,
    response_date DATE,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
"""

def create_database_connection():
    try:
        connection = sqlite3.connect(DATABASE_CONNECTION_STRING)
        connection.row_factory = sqlite3.Row
        return connection, ""
    except sqlite3.DatabaseError as e:
        return None, str(e)

def initialize_database():
    db_conn, error = create_database_connection()
    if db_conn is None:
        print(f"Failed to connect to the database: {error}")
        return
    try:
        db_cursor = db_conn.cursor()
        db_cursor.executescript(DATABASE_SCHEMA)
        db_conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Failed to initialize the database: {e}")
    finally:
        db_conn.close()

def create_user(username, password, email):
    db_conn, error = create_database_connection()
    if db_conn is None:
        return False, f"Failed to connect to the database: {error}"
    try:
        db_cursor = db_conn.cursor()
        db_cursor.execute(
            'INSERT INTO user (username, password, email) VALUES (?, ?, ?)',
            (username, password, email)
        )
        db_conn.commit()
        return True, ""
    except sqlite3.DatabaseError as e:
        return False, str(e)
    finally:
        db_conn.close()

def create_job_application(user_id, company_name, position, status, application_date, response_date=None, notes=None):
    db_conn, error = create_database_connection()
    if db_conn is None:
        return False, f"Failed to connect to the database: {error}"
    try:
        db_cursor = db_conn.cursor()
        db_cursor.execute(
            'INSERT INTO application (user_id, company_name, position, status, application_date, response_date, notes) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (user_id, company_name, position, status, application_date, response_date, notes)
        )
        db_conn.commit()
        return True, ""
    except sqlite3.DatabaseError as e:
        return False, str(e)
    finally:
        db_conn.close()

def fetch_applications_by_user(user_id):
    db_conn, error = create_database_connection()
    if db_conn is None:
        print(f"Failed to connect to the database: {error}")
        return []
    try:
        db_cursor = db_conn.cursor()
        db_cursor.execute('SELECT * FROM application WHERE user_id = ?', (user_id,))
        applications = db_cursor.fetchall()
        return applications
    except sqlite3.DatabaseError as e:
        print(f"Failed to fetch applications: {e}")
        return []
    finally:
        db_conn.close()

def update_job_application_status(application_id, new_status):
    db_conn, error = create_database_connection()
    if db_conn is None:
        return False, f"Failed to connect to the database: {error}"
    try:
        db_cursor = db_conn.cursor()
        db_cursor.execute(
            'UPDATE application SET status = ? WHERE id = ?',
            (new_status, application_id)
        )
        db_conn.commit()
        return True, ""
    except sqlite3.DatabaseError as e:
        return False, str(e)
    finally:
        db_conn.close()

if __name__ == "__main__":
    initialize_database()
    print("Database initialized and tables created.")