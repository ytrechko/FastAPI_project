from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models.db_models import Item, UserItem
from schemas.obj_schemas import ItemCreate, ItemRead, ItemUpdate


async def create_item(item: ItemCreate, db: AsyncSession):
    db_item = Item(title=item.title, description=item.description)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)


async def read_all_items(db: AsyncSession) -> List[ItemRead]:
    stmt_get = select(Item)
    result = await db.execute(stmt_get)
    items = result.scalars().all()
    return items


async def update_item(id: int, item: ItemUpdate, db: AsyncSession):
    stmt = select(Item).where(Item.id == id)
    result = await db.execute(stmt)
    availability_item = result.scalar_one_or_none()
    if not availability_item:
        raise HTTPException(status_code=404, detail=f"Item with {id} is not found")

    stmt = (
        update(Item).where(Item.id == id).values(**item.model_dump(exclude_unset=True))
    )
    await db.execute(stmt)
    await db.commit()


async def delete_item(id_item: int, db: AsyncSession):
    stmt_availability_item = select(Item).where(Item.id == id_item)
    result = await db.execute(stmt_availability_item)
    availability_item = result.scalar_one_or_none()
    if not availability_item:
        raise HTTPException(status_code=404, detail=f"Item with {id_item} not found")

    stmt_delete_links = delete(UserItem).where(UserItem.id_item == id_item)
    await db.execute(stmt_delete_links)

    stmt_delete_item = delete(Item).where(Item.id == id_item)
    await db.execute(stmt_delete_item)

    await db.commit()
