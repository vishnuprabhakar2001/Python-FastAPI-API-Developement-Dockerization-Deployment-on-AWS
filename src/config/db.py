from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = None
db = None


def connect_db():
    global client, db

    mongo_uri = os.getenv("MONGO_URI")

    client = MongoClient(mongo_uri)

    db = client["userDB"]

    print("MongoDB Connected")


def get_db():
    return db