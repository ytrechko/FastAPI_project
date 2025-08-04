from fastapi import HTTPException
from sqlalchemy import select, update, delete, and_

from schemas.obj_schemas import UserItemCreate, UserItemUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_models import User, Item, UserItem


async def link_user_item(user_item: UserItemCreate, db: AsyncSession ):

    stmt = select(User).where(User.id == user_item.id_user)
    result = await db.execute(stmt)
    is_user = result.scalar_one_or_none()
    if not is_user:
        raise HTTPException(status_code=404, detail=f"User with {user_item.id_user} id is not found")

    stmt = select(Item).where(Item.id == user_item.id_item)
    result = await db.execute(stmt)
    is_item = result.scalar_one_or_none()
    if not is_item:
        raise HTTPException(status_code=404, detail=f"Item with {user_item.id_item} id is not found")

    db_user_item = UserItem( id_user=user_item.id_user, id_item=user_item.id_item)
    db.add(db_user_item)
    await db.commit()
    await db.refresh(db_user_item)

async def update_link_user_item(id_user: int, id_item: int , update_user_item: UserItemUpdate, db: AsyncSession):

    stmt = select(UserItem).where(and_(UserItem.id_user == id_user , UserItem.id_item == id_item))
    result = await db.execute(stmt)
    availability_user_with_item = result.scalar_one_or_none()
    if not availability_user_with_item:
        raise HTTPException(status_code=404, detail=f"User {id_user} id  with item {id_item} id is not found")

    stmt = select(Item).where(Item.id == update_user_item.id_item)
    result = await db.execute(stmt)
    availability_item = result.scalar_one_or_none()
    if not availability_item:
        raise HTTPException(status_code=404, detail=f"Item with {update_user_item.id_item} id is not found")


    stmt = update(UserItem).where(and_(UserItem.id_user == id_user , UserItem.id_item == id_item)).values(id_item=update_user_item.id_item)
    await db.execute(stmt)
    await db.commit()

async def delete_user_item(id_user: int, id_item: int, db: AsyncSession):

    stmt_availability = select(UserItem).where(and_(UserItem.id_user == id_user , UserItem.id_item == id_item))
    result = await db.execute(stmt_availability)
    availability_user_with_item = result.scalar_one_or_none()
    if not availability_user_with_item:
        raise HTTPException(status_code=404, detail=f"User {id_user} id  with item {id_item} id is not found")

    stmt_delete = delete(UserItem).where(and_(UserItem.id_user == id_user , UserItem.id_item == id_item))
    await db.execute(stmt_delete)
    await db.commit()
