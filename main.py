from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy.orm import  joinedload
from contextlib import asynccontextmanager
from typing import List

from database import Base, engine, asuncSessionLocal
from obj_schemas import UserCreate, UserRead,\
                        ItemCreate, ItemRead,\
                        ItemUserCreate, ItemUserRead,\
                        UserWithItemsRead
from db_models import Item, User, ItemUser


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield

app = FastAPI(lifespan=lifespan)


async def get_db():
    async with asuncSessionLocal() as session:
        yield session

@app.post("/user/", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user

@app.post("/item/", response_model=ItemRead)
async def create_item(item: ItemCreate,  db: AsyncSession = Depends(get_db)) -> Item:
    db_item = Item(title=item.title, description=item.description)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)

    return db_item

@app.post("/link-item-user/", response_model=ItemUserRead)
async def link_item_user(item_user: ItemUserCreate, db: AsyncSession = Depends(get_db)) -> ItemUser:

    stmt = select(User).where(User.id == item_user.id_user)
    result = await db.execute(stmt)
    is_user = result.scalar_one_or_none()
    if not is_user:
        raise HTTPException(status_code=404, detail=f"User with {item_user.id_user} id is not found")

    stmt = select(Item).where(Item.id == item_user.id_item)
    result = await db.execute(stmt)
    is_item = result.scalar_one_or_none()
    if not is_item:
        raise HTTPException(status_code=404, detail=f"Item with {item_user.id_item} id is not found")

    db_item_user = ItemUser(id_item=item_user.id_item, id_user=item_user.id_user)
    db.add(db_item_user)
    await db.commit()
    await db.refresh(db_item_user)

    return db_item_user

@app.get("/user/{id}", response_model=UserWithItemsRead)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(User).\
            options(joinedload(User.items)).\
            where(User.id == id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@app.get("/users/", response_model=List[UserWithItemsRead])
async def get_users(db: AsyncSession = Depends(get_db)):
    stmt = select(User).options(joinedload(User.items))
    result = await db.execute(stmt)
    users = result.unique().scalars().all()

    return users
