from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from schemas.obj_schemas import UserItemCreate, UserItemUpdate
from database.session import get_db
from crud.user_item import link_user_item, update_link_user_item, delete_user_item

router = APIRouter(prefix="/user-items", tags=["user-items"])

@router.post("/link-user-item/")
async def link_user_item_route(user_item: UserItemCreate, db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    await link_user_item(user_item, db)
    return {"status" : "link user-item successful created"}

@router.put("/users/{id_user}/items/{id_item}")
async def update_link_user_item_route(id_user: int, id_item: int , update_user_item: UserItemUpdate, db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    await update_link_user_item(id_user, id_item, update_user_item, db)
    return {"status" : "link user-item successful updated"}

@router.delete("/users/{id_user}/items/{id_item}")
async def delete_user_item_route(id_user: int, id_item: int, db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    await delete_user_item(id_user, id_item, db)
    return {"status" : "link user-item successful deleted"}
