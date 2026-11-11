from fastapi import FastAPI
from sqlalchemy import text

from app.database.session import engine

app = FastAPI(
    title="AI Examination System API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "AI Examination System API is running"}


@app.get("/health/database")
def database_health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"database": "connected"}