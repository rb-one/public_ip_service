import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import BasicConfig

basic_config = BasicConfig()


class EmailSender:
    """Email sender class"""

    def __init__(self, subject="", message=""):
        self.email_sender = basic_config.EMAIL_SENDER
        self.email_password = basic_config.EMAIL_PASSWORD
        self.subject = subject
        self.message = message

    def build_email(self):
        """Creates the template for the email"""
        # Create message object instance
        self.msg = MIMEMultipart()
        self.msg["From"] = self.email_sender
        self.msg["To"] = self.email_sender
        self.msg["Subject"] = self.subject

        # Email body
        self.message = self.message
        self.msg.attach(MIMEText(self.message, "plain"))

    def create_server(self):
        """Create the connection server"""
        # create server
        self.server = smtplib.SMTP("smtp.gmail.com: 587")
        self.server.starttls()
        # Login Credentials for sending the mail
        self.server.login(self.msg["From"], self.email_password)

    def send_email(self):
        """Calls sends the email using the other methods"""
        self.build_email()
        self.create_server()

        # send the message via the server.
        self.server.sendmail(self.msg["From"], self.msg["To"], self.msg.as_string())
        self.server.quit()

        # TODO add to logs instead of print
        print("successfully sent email to %s:" % (self.msg["To"]))
