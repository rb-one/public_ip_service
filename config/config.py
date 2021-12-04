import os

from dotenv import load_dotenv

load_dotenv()


class BasicConfig:
    URL = os.environ.get("URL")
    
    EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    
    LOCAL_PATH = os.environ.get("LOCAL_PATH")
    REMOTE_PATH = os.environ.get("REMOTE_PATH")
    
    LOCAL_PUBLIC_IP_FILE = LOCAL_PATH + os.environ.get("LOCAL_PUBLIC_IP_FILE")
    FOREIGN_PUBLIC_IP_FILE = LOCAL_PATH + os.environ.get("FOREIGN_PUBLIC_IP_FILE")
