from dotenv import load_dotenv
import os
import uvicorn

from src.config.db import connect_db
from src.app import app

load_dotenv()

PORT = int(os.getenv("PORT", 8000))


@app.on_event("startup")
async def startup_event():
    connect_db()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=PORT, reload=True)