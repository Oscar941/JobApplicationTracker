import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH', 'job_applications.db')

class DBConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            return self.conn
        except sqlite3.Error as e:
            print(e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

def add_application(application_details):
    with DBConnection(DATABASE_PATH) as conn:
        sql = '''INSERT INTO applications(company_name, position, date_applied, status, notes)
                 VALUES(?,?,?,?,?)'''
        try:
            cur = conn.cursor()
            cur.execute(sql, (application_details['company_name'], application_details['position'],
                              application_details['date_applied'], application_details['status'],
                              application_details['notes']))
            conn.commit()
        finally:
            cur.close()

def get_applications():
    with DBConnection(DATABASE_PATH) as conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM applications")
            applications = cur.fetchall()
            return applications
        finally:
            cur.close()

def update_application(app_id, updates):
    with DBConnection(DATABASE_PATH) as conn:
        sql = "UPDATE applications SET "
        sql += ', '.join([f"{column} = ?" for column in updates.keys()])
        sql += " WHERE id = ?"
        try:
            cur = conn.cursor()
            cur.execute(sql, list(updates.values()) + [app_id])
            conn.commit()
        finally:
            cur.close()

def change_status(app_id, new_status):
    update_application(app_id, {'status': new_status})