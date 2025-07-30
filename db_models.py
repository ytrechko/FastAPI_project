from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class TableUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)

class TableItem(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

class TableItemUser(Base):
    __tablename__ = "items_users"

    id_item = Column(Integer, ForeignKey("items.id"), primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id"), primary_key=True)
