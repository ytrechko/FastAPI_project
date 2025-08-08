from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class FileBase(BaseModel):
    filename: str
    owner_id: int


class FileCreate(FileBase):
    pass


class FileRead(FileBase):
    id: int
    path: str
    uploadet_at: datetime

    class Config:
        from_attributes = True
