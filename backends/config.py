import os
import secrets
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ADMIN_USER = os.getenv("ADMIN_USER")
    ADMIN_PASS = os.getenv("ADMIN_PASS")

    if not ADMIN_USER or not ADMIN_PASS or not MONGO_URI or not JWT_SECRET_KEY:
        raise ValueError("MONGO_URI, JWT_SECRET_KEY, ADMIN_USER, and ADMIN_PASS must be set in environment variables.")
