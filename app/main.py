from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import auth, categories, orders, products, profiles, users
from app.db.database import AsyncSessionLocal
from app.db.seed import seed_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with AsyncSessionLocal() as session:
        await seed_data(session)
    yield


app = FastAPI(title="FastAPI", lifespan=lifespan)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(profiles.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/")
def root():
    return {"status": "ok"}