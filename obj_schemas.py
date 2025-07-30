from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    pass


class ItemBase(BaseModel):
    title: str
    description: str
    id_owner: int

class ItemCreate(ItemBase):
    id: int

    class Config:
        from_attributes = True

class ItemRead(ItemBase):
    pass
