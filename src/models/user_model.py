from src.config.db import get_db


def get_user_collection():
    db = get_db()

    if db is None:
        raise Exception("Database not connected")

    return db["users"]