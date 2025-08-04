from fastapi import FastAPI

from contextlib import asynccontextmanager

from database.session import Base, engine
from api import users, items, users_items, forms

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(forms.router)
app.include_router(items.router)
app.include_router(users.router)
app.include_router(users_items.router)
