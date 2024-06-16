import sqlite3
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = getenv('DATABASE_URL')

SCHEMA = """
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
    position TEXT NOT NULL,
    status TEXT NOT NULL,
    application_date DATE,
    response_date DATE,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
"""

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executescript(SCHEMA)
    conn.commit()
    conn.close()

def add_user(username, password, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO user (username, password, email) VALUES (?, ?, ?)',
        (username, password, email)
    )
    conn.commit()
    conn.close()

def add_application(user_id, company_name, position, status, application_date, response_location=None,  notes=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO application (user_id, company_name, position, status, application_date, response_date, notes) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (user_id, company_name, position, status, application_date, response_location, notes)
    )
    conn.commit()
    conn.close()

def get_applications_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM application WHERE user_id = ?', (user_id,))
    applications = cursor.fetchall()
    conn.close()
    return applications

def update_application_status(application_id, new_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE application SET status = ? WHERE id = ?',
        (new_status, application_id)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized and tables created.")