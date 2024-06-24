import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

SENDER_EMAIL = os.getenv('EMAIL_USER')
SENDER_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))

def send_email(recipient, subject, body):
    try:
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.starttls()
        session.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = message.as_string()
        session.sendmail(SENDER_EMAIL, recipient, text)
        session.quit()
        print('Mail Sent to', recipient)
    except Exception as e:
        print('Mail sending failed:', e)

def application_status_update(user_email, application):
    subject = f"Update on Your Application for {application['position']} at {application['company']}"
    body = f"Dear {application['applicant_name']},\n\nWe are pleased to inform you that the status of your application for {application['position']} at {application['company']} has been updated to {application['status']}.\n\nRegards,\nJobApplicationTracker Team"
    send_email(user_email, subject, body)

def interview_reminder(user_email, interview):
    subject = f"Interview Reminder: {interview['company']} - {interview['position']}"
    body = f"Dear {interview['applicant_name']},\n\nJust a friendly reminder about your upcoming interview for {interview['position']} at {interview['company']} on {interview['date']} at {interview['time']}.\n\nGood luck!\n\nRegards,\nJobApplicationTracker Team"
    send_email(user_email, subject, body)

def send_general_notification(user_email, subject, message):
    body = f"Hi,\n\n{er_email(user_email, subject, body)