from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

class ForTableUser(UserBase):
    id: int

    class Config:
        from_attributes = True

class ForObjUser(UserBase):
    pass


class ItemBase(BaseModel):
    title: str
    description: str
    id_owner: int

class ForTableItem(ItemBase):
    id: int

    class Config:
        from_attributes = True

class ForObjItem(ItemBase):
    pass
