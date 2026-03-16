from fastapi import FastAPI
from src.routes.user_routes import router as user_router

app = FastAPI()

# Routes
app.include_router(user_router, prefix="/api")