# config.py
import os
from dotenv import load_dotenv

# Load variables from .env file into os.environ
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise Exception("DATABASE_URL environment variable is not set.")

# Other configuration variables can go here as needed.
