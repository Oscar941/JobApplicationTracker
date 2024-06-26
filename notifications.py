import os
from dotenv import load_env
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

EMAIL_SENDER_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_SENDER_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
EMAIL_SMTP_PORT = int(os.getenv('SMTP_PORT', 587))

def dispatch_email(recipient_address, email_subject, email_content):
    try:
        email_message = MIMEMultipart()
        email_message['From'] = EMAIL_SENDER_ADDRESS
        email_message['To'] = recipient_address
        email_message['Subject'] = email_subject
        email_message.attach(MIMEText(email_content, 'plain'))

        smtp_session = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
        smtp_session.starttls()
        smtp_session.login(EMAIL_SENDER_ADDRESS, EMAIL_SENDER_PASSWORD)
        
        final_email_text = email_message.as_string()
        smtp_session.sendmail(EMAIL_SENDER_ADDRESS, recipient_address, final_email_text)
        smtp_session.quit()
        print('Email successfully sent to', recipient_address)
    
    except Exception as error:
        print('Failed to send email:', error)

def notify_application_status_update(applicant_email, application_details):
    email_subject = f"Update on Your Application for {application_details['position']} at {application_details['company']}"
    email_body = f"Dear {application_details['applicant_name']},\n\nWe are pleased to inform you that the status of your application for {application_details['position']} at {application_details['company']} has been updated to {application_details['status']}.\n\nBest Regards,\nJobApplicationTracker Team"
    dispatch_email(applicant_email, email_subject, email_body)

def send_interview_reminder(applicant_email, interview_details):
    email_subject = f"Interview Reminder: {interview_details['company']} - {interview_details['position']}"
    email_body = f"Dear {interview_details['applicant_name']},\n\nJust a friendly reminder about your upcoming interview for {interview_details['position']} at {interview_details['company']} on {interview_details['date']} at {interview_details['time']}.\n\nGood luck!\n\nBest Regards,\nJobApplicationTracker Team"
    dispatch_email(applicant_email, email_subject, email_body)

def dispatch_general_notification(recipient_email, notification_subject, notification_message):
    email_body = f"Hi,\n\n{notification_message}\n\nBest Regards,\nJobApplicationTracker Team"
    dispatch_email(recipient_email, notification_subject, email_body)