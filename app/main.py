import os

from fastapi import FastAPI
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@db:5432/postgres",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

app = FastAPI()


@app.get("/")
def main():
    return {"Hello": "World"}


@app.get("/db-health")
def db_health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}