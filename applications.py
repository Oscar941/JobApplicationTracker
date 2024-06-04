import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH', 'job_applications.db')

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
    except sqlite3.Error as e:
        print(e)
    return conn

def add_application(application_details):
    conn = create_connection()
    sql = '''INSERT INTO applications(company_name, position, date_applied, status, notes)
             VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, (application_details['company_name'], application_details['position'],
                      application_details['date_applied'], application_details['status'],
                      application_details['notes']))
    conn.commit()
    conn.close()

def get_applications():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM applications")
    applications = cur.fetchall()
    conn.close()
    return applications

def update_application(app_id, updates):
    conn = create_connection()
    sql = f"UPDATE applications SET "
    sql += ', '.join([f"{column} = ?" for column in updates.keys()])
    sql += " WHERE id = ?"
    cur = conn.cursor()
    cur.execute(sql, list(updates.values()) + [app_id])
    conn.commit()
    conn.close()

def change_status(app_id, new_status):
    update_application(app_id, {'status': new_status})