import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH', 'job_applications.db')

class DatabaseConnector:
    def __init__(self, database_path):
        self.database_path = database_path
        self.connection = None

    def __enter__(self):
        try:
            self.connection = sqlite3.connect(self.database_path)
            return self.connection
        except sqlite3.Error as error:
            print(error)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

def insert_application(application_data):
    with DatabaseConnector(DATABASE_PATH) as connection:
        insert_query = '''INSERT INTO applications(company_name, position, date_applied, status, notes)
                          VALUES(?,?,?,?,?)'''
        try:
            cursor = connection.cursor()
            cursor.execute(insert_query, (application_data['company_name'], application_data['position'],
                                          application_data['date_applied'], application_data['status'],
                                          application_data['notes']))
            connection.commit()
        finally:
            cursor.close()

def fetch_applications():
    with DatabaseConnector(DATABASE_PATH) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM applications")
            applications = cursor.fetchall()
            return applications
        finally:
            cursor.close()

def modify_application(application_id, modifications):
    with DatabaseConnector(DATABASE_PATH) as connection:
        update_query = "UPDATE applications SET "
        update_query += ', '.join([f"{field} = ?" for field in modifications.keys()])
        update_nguery += " WHERE id = ?"
        try:
            cursor = connection.cursor()
            cursor.execute(update_query, list(modifications.values()) + [application_id])
            connection.commit()
        finally:
            cursor.close()

def update_application_status(application_id, status_update):
    modify_application(application_id, {'status': status_update})