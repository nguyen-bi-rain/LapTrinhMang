import getpass
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587  # Use port 587 for TLS


def send_email(sender, receipt):
    msg = MIMEMultipart()
    msg['To'] = receipt
    msg['From'] = sender
    subject = input("Enter subject: ")
    msg['Subject'] = subject
    message = input("Email content: ")

    # Create the email part
    part = MIMEText(message, 'plain')
    msg.attach(part)

    try:
        # Connect to the server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as session:
            session.starttls()  # Upgrade the connection to secure
            session.ehlo()
            password = getpass.getpass(prompt='Password for {}: '.format(sender))
            session.login(sender, password)
            session.sendmail(sender, receipt, msg.as_string())
            print("Your email is sent to {0}".format(receipt))
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    sender = input("From address: ")
    receipt = input("To address: ")
    send_email(sender, receipt)
