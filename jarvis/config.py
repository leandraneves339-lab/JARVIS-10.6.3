import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("JARVIS_NAME", "JARVIS 10.6")
WAKE_WORD = os.getenv("JARVIS_WAKE_WORD", "jarvis")
API_KEY = os.getenv("JARVIS_API_KEY", "")
API_URL = os.getenv("JARVIS_API_URL", "")
DATA_DIR = os.getenv("JARVIS_DATA_DIR", ".")
