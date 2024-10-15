import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS")
if not MONGO_DETAILS:
    raise ValueError("MONGO_DETAILS environment variable is not set.")

DATABASE_NAME = os.getenv("DATABASE_NAME")
if not DATABASE_NAME:
    raise ValueError("DATABASE_NAME must be defined.")

BACDIVE_EMAIL = os.getenv("BACDIVE_EMAIL")
if not BACDIVE_EMAIL:
    raise ValueError("BACDIVE_EMAIL must be defined.")

BACDIVE_PASSWORD = os.getenv("BACDIVE_PASSWORD")
if not BACDIVE_PASSWORD:
    raise ValueError("BACDIVE_PASSWORD must be defined.")

HOST = os.getenv("HOST")
if not HOST:
    raise ValueError("HOST must be defined.")

PORT = os.getenv("PORT")
if not PORT:
    raise ValueError("PORT must be defined.")

OPERATIONS_FOLDERS = os.getenv("OPERATIONS_FOLDERS")
if not OPERATIONS_FOLDERS:
    raise ValueError("OPERATIONS_FOLDERS must be defined.")

DEBUG = os.getenv("DEBUG")
if not DEBUG:
    raise ValueError("DEBUG must be defined.")

API_PREFIX = os.getenv("API_PREFIX")
if not API_PREFIX:
    raise ValueError("API_PREFIX must be defined.")