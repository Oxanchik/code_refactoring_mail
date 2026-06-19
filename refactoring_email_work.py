import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

from dotenv import load_dotenv

class EmailClient:
    def __init__(self, smtp_server, smtp_port, imap_server, login, password):
        """Initialize the email client with server details and credentials."""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.imap_server = imap_server
        self.login = login
        self.password = password

    def send_email(self, recipients, subject, message_text):
        """Send an email to a list of recipients."""
        server = None

        # Create the message
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message_text, 'plain'))

        # Connect and send
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.login, self.password)
            server.sendmail(self.login, recipients, msg.as_string())
            print(f"Email sent successfully to {recipients}")
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            if server:
                server.quit()

    def receive_emails(self, subject_header=None):
        """
        Connect to IMAP server and fetch emails.
        If subject_header is provided, searches for specific subject.
        Returns the latest matching email message or None.

        """
        mail = None
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.login, self.password)
            mail.list()
            mail.select("inbox")

            # Define search criterion
            if subject_header:
                criterion = f'(HEADER Subject "{subject_header}")'
            else:
                criterion = 'ALL'

            result, data = mail.uid('search', "", criterion)

            if not data[0]:
                print("No letters found with current header.")
                return None

            # Get the latest email UID
            latest_email_uid = data[0].split()[-1]
            result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')

            raw_email = data[0][1]
            email_message = email.message_from_bytes(raw_email)

            return email_message

        except Exception as e:
            print(f"Failed to receive email: {e}")
            return None
        finally:
            if mail:
                mail.logout()

if __name__ == '__main__':
    # Configuration values
    load_dotenv()
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = os.getenv("SMTP_PORT", "587")
    IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
    USER_LOGIN = os.getenv("USER_LOGIN", "login@gmail.com")
    USER_PASSWORD = os.getenv("USER_PASSWORD", "qwerty")

    # Initialize the client
    client = EmailClient(SMTP_SERVER, SMTP_PORT, IMAP_SERVER, USER_LOGIN, USER_PASSWORD)

    # Send an email
    recipients_list = ['vasya@email.com', 'petya@email.com']
    email_subject = 'Refactored Subject'
    email_body = 'This is a refactored message.'

    client.send_email(recipients_list, email_subject, email_body)

    # Receive an email
    search_subject = 'Refactored Subject'
    received_msg = client.receive_emails(subject_header=search_subject)

    if received_msg:
        print(f"From: {received_msg['From']}")
        print(f"Subject: {received_msg['Subject']}")
