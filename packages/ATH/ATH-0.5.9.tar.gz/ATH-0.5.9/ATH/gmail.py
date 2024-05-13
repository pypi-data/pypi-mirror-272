from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from imaplib import IMAP4_SSL
import email

def send_email(email, app_password, to_email, name, subject, message):
    msg = MIMEMultipart()
    txt = MIMEText(message)
    msg.attach(txt)
    msg["subject"] = subject
    msg["from"] = name
    with SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(email, app_password)
        smtp.sendmail(email, to_email, msg.as_string())

def receive_email(Gmail, app_password):
    with IMAP4_SSL("imap.gmail.com") as imap:
        imap.login(Gmail, app_password)
        imap.select("INBOX")
        _, data = imap.search(None, "ALL")
        for num in data[0].split():
            _, data = imap.fetch(num, "(RFC822)")
            _, bytes_data = data[0]
            email_message = email.message_from_bytes(bytes_data)
            print("Subject: ", email_message["subject"])