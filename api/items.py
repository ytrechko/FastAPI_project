from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List

from models.db_models import Item
from schemas.obj_schemas import ItemCreate, ItemRead, ItemUpdate
from database.session import get_db
from crud.item import create_item, read_all_items, update_item, delete_item

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/items/")
async def create_item_route(
    item: ItemCreate, db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:

    await create_item(item, db)
    return {"status": "item successful created"}


@router.get("/items/", response_model=List[ItemRead])
async def read_all_items_route(db: AsyncSession = Depends(get_db)) -> List[ItemRead]:
    return await read_all_items(db)


@router.put("/items/{id}")
async def update_item_route(
    id: int, item: ItemUpdate, db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    await update_item(id, item, db)
    return {"status": "item successful updated"}


@router.delete("/item/{id_item}")
async def delete_item_route(
    id_item: int, db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    await delete_item(id_item, db)
    return {"status": "item successful deleted"}
