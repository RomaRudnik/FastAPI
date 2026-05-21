from fastapi import FastAPI

from app.api.routers import users

app = FastAPI(title="FastAPI")

app.include_router(users.router)


@app.get("/")
def root():
    return {"status": "ok"}