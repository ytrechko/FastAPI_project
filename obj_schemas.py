from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str

class ItemRead(ItemBase):
    id: int

    class Config:
        from_attributes = True

class ItemCreate(ItemBase):
    pass



class UserBase(BaseModel):
    name: str
    email: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    pass



class ItemUserBase(BaseModel):
    id_item: int
    id_user: int

class ItemUserCreate(ItemUserBase):
    pass

class ItemUserRead(ItemUserBase):
    class Config:
        from_attributes = True


class UserWithItemsRead(UserRead):
    items: list[ItemRead] = []
