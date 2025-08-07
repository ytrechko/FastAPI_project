from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List

from schemas.obj_schemas import UserCreate, UserRead, UserUpdate, UserWithItemsRead
from database.session import get_db
from crud.user import create_user, read_user, read_all_users, update_user, delete_user


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def create_user_route(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    await create_user(user, db)
    return {"status": "user successful created"}


@router.get("/{id_user}", response_model=UserWithItemsRead)
async def read_user_route(
    id_user: int, db: AsyncSession = Depends(get_db)
) -> UserWithItemsRead:
    return await read_user(id_user, db)


@router.get("/", response_model=List[UserWithItemsRead])
async def read_all_users_route(
    db: AsyncSession = Depends(get_db),
) -> List[UserWithItemsRead]:
    return await read_all_users(db)


@router.put("/{id}/")
async def update_user_route(
    id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    await update_user(id, user, db)
    return {"status": "user successful updated"}


@router.delete("/{id_user}")
async def delete_user_route(
    id_user: int, db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    await delete_user(id_user, db)
    return {"status": "user successful deleted"}
