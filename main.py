from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from database import Base, engine, db_session
from obj_schemas import UserCreate, UserRead,\
                        ItemCreate, ItemRead,\
                        ItemUserCreate, ItemUserRead,\
                        UserWithItemsRead
from db_models import Item, User, ItemUser
app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    with db_session() as session:
        yield session

@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post("/item/", response_model=ItemRead)
def create_item(item: ItemCreate,  db: Session = Depends(get_db)) -> Item:
    db_item = Item(title=item.title, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

@app.post("/link-item-user/", response_model=ItemUserRead)
def link_item_user(item_user: ItemUserCreate, db: Session = Depends(get_db)) -> ItemUser:
    if not db.query(User).filter(User.id == item_user.id_user).first():
        raise HTTPException(status_code=404, detail=f"User with {item_user.id_user} id is not found")
    if not db.query(Item).filter(Item.id == item_user.id_item).first():
        raise HTTPException(status_code=404, detail=f"Item with {item_user.id_item} id is not found")

    db_item_user = ItemUser(id_item=item_user.id_item, id_user=item_user.id_user)
    db.add(db_item_user)
    db.commit()
    db.refresh(db_item_user)

    return db_item_user

@app.get("/user/{id}", response_model=UserWithItemsRead)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(User).\
              options(joinedload(User.items)).\
              filter(User.id == id).\
              first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
