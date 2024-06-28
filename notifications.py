import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

EMAIL_SENDER_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_SENDER_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
EMAIL_SMTP_PORT = int(os.getenv('SMTP_PORT', 587))

class EmailDispatcher:
    def __init__(self, server, port, user, password):
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.session = None

    def start_session(self):
        if self.session is None:
            self.session = smtplib.SMTP(self.server, self.port)
            self.session.starttls()
            self.session.login(self.user, self.password)

    def send_email(self, recipient_address, email_subject, email_content):
        try:
            email_message = MIMEMultipart()
            email_message['From'] = EMAIL_SENDER_ADDRESS
            email_message['To'] = recipient_address
            email_message['Subject'] = email_subject
            email_message.attach(MIMEText(email_content, 'plain'))

            final_email_text = email_message.as_string()
            self.session.sendmail(EMAIL_SENDER_ADDRESS, recipient_ address, final_email_text)
            print('Email successfully sent to', recipient_address)

        except Exception as error:
            print('Failed to send email:', error)
    
    def end_session(self):
        if self.session is not None:
            self.session.quit()
            self.session = None

email_dispatcher = EmailDispatcher(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT, EMAIL_SENDER_ADDRESS, EMAIL_SENDER_PASSWORD)

def notify_applicants(applicant_emails, email_subject, email_content_func):
    email_dispatcher.start_session()
    
    for applicant_email, details in applicant_emails.items():
        email_body = email_content_func(details)
        email_dispatcher.send_email(applicant_email, email_subject(details), email_body)
    
    email_dispatcher.end_session()

applicant_emails = {
    # email: application_details,
}

def application_status_subject(details):
    return f"Update on Your Application for {details['position']} at {details['company']}"

def application_status_body(details):
    return f"Dear {details['applicant_name']},\n\nWe are pleased to inform you that the status of your application for {details['position']} at {pdetails['company']} has been updated to {details['status']}.\n\nBest Regards,\nJobApplicationTracker Team"

notify_applicants(applicant_emails, application_status_subject, application_status_body)