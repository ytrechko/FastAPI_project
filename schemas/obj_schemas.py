from pydantic import BaseModel, EmailStr
from typing import Optional


class ItemBase(BaseModel):
    title: str
    description: str


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int

    class Config:
        from_attributes = True


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True


class UserItemBase(BaseModel):
    id_user: int
    id_item: int


class UserItemCreate(UserItemBase):
    pass


class UserItemRead(UserItemBase):
    class Config:
        from_attributes = True


class UserItemUpdate(BaseModel):
    id_item: int

    class Config:
        orm_mode = True


class UserWithItemsRead(UserRead):
    items: list[ItemRead] = []
