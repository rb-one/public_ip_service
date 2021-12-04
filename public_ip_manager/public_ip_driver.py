import os

import requests
from paramiko import SSHClient
from requests import ConnectionError
from scp import SCPClient

from email_sender import EmailSender

from config import BasicConfig

basic_config = BasicConfig()

class PublicIpDriver:
    def __init__(self):
        """init method"""
        self.url = basic_config.URL
        self.local_public_ip_file = basic_config.LOCAL_PUBLIC_IP_FILE
        self.foreing_public_ip_file = basic_config.FOREIGN_PUBLIC_IP_FILE

    def get_local_public_ip(self):
        """Get the public ip from a trusted page"""

        try:
            self.current_local_public_ip = requests.get(self.url).text

        except ConnectionError as err:
            # Send Email notification
            LOGNAME = os.environ.get("LOGNAME")
            self.current_local_public_ip

            subject = f"ConnectionError on {LOGNAME}"
            message = err

            mail = EmailSender(subject=subject, message=message)
            mail.send_email()


    def read_stored_local_public_ip(self):
        """Reads the stored local ip"""

        try:
            with open(self.local_public_ip_file, "r") as f:
                self.stored_local_public_ip = f.read()

        except FileNotFoundError:
            pass

    def read_stored_foreing_public_ip(self):
        """Reads the stored foreing ip"""

        try:
            with open(self.foreing_public_ip_file, "r") as f:
                stored_foreign_public_ip = f.read()
                return stored_foreign_public_ip

        except FileNotFoundError:
            pass

    def write_current_public_ip(self):
        """Writes the stored ip"""

        with open(self.local_public_ip_file, "w") as f:
            f.write(self.current_local_public_ip)

    def send_current_local_public_ip_file_by_ssh(self):
        """Share the local_current_public_ip with the destiny machine"""

        CLIENT_NAME = os.environ.get("CLIENT_NAME")
        SHH_KEY = os.environ.get("SSH_KEY")
        PORT = os.environ.get("PORT")
        PASSPHRASE = os.environ.get("PASSPHRASE")
        REMOTE_PATH = os.environ.get("REMOTE_PATH")

        src_file = self.local_public_ip_file
        client_ip = self.read_stored_foreing_public_ip()

        ssh = SSHClient()
        ssh.load_system_host_keys()

        # Create ssh connection
        ssh.connect(
            hostname=client_ip,
            port=int(PORT),
            username=CLIENT_NAME,
            key_filename=SHH_KEY,
            passphrase=PASSPHRASE,
        )

        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(ssh.get_transport())

        # Uploading the 'test' directory with its content in the remote directory
        scp.put(src_file, recursive=False, remote_path=REMOTE_PATH)
        scp.close()

    def send_current_local_public_ip_file_by_email(self):
        """Share the local_current_public_ip with by email"""

        LOGNAME = os.environ.get("LOGNAME")
        self.current_local_public_ip

        subject = f"Public IP has change for this {LOGNAME}"
        message = f"The new public ip is {self.current_local_public_ip}"

        mail = EmailSender(subject=subject, message=message)
        mail.send_email()

    def process(self):
        """To be overriden by the child"""

        pass
