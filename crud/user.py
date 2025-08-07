from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from typing import List

from schemas.obj_schemas import UserCreate, UserRead, UserUpdate, UserWithItemsRead
from models.db_models import User, UserItem


async def create_user(user: UserCreate, db: AsyncSession):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)


async def read_user(id_user: int, db: AsyncSession) -> UserWithItemsRead:
    stmt = select(User).options(joinedload(User.items)).where(User.id == id_user)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def read_all_users(db: AsyncSession) -> List[UserWithItemsRead]:
    stmt = select(User).options(joinedload(User.items))
    result = await db.execute(stmt)
    users = result.unique().scalars().all()

    return users


async def update_user(id: int, user: UserUpdate, db: AsyncSession):
    stmt = select(User).where(User.id == id)
    result = await db.execute(stmt)
    availability_user = result.scalar_one_or_none()
    if not availability_user:
        raise HTTPException(status_code=404, detail=f"User with {id} is not found")

    stmt = (
        update(User).where(User.id == id).values(**user.model_dump(exclude_unset=True))
    )
    await db.execute(stmt)
    await db.commit()


async def delete_user(id_user: int, db: AsyncSession):
    stmt_availability_user = select(User).where(User.id == id_user)
    result = await db.execute(stmt_availability_user)
    availability_user = result.scalar_one_or_none()
    if not availability_user:
        raise HTTPException(status_code=404, detail=f"User with {id_user} not found")

    stmt_delete_links = delete(UserItem).where(UserItem.id_user == id_user)
    await db.execute(stmt_delete_links)

    stmt_delete_user = delete(User).where(User.id == id_user)
    await db.execute(stmt_delete_user)

    await db.commit()
