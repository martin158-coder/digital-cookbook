import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET")
    MONGO_DBNAME = os.getenv("DBNAME")
    MONGO_URI = os.getenv("URI")