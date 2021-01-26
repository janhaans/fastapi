from fastapi import FastAPI, Path, HTTPException, Depends
from sqlalchemy.orm import Session

from typing import List

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/item/{name}", response_model=schemas.Item)
def get_item(name: str, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_name=name)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.post("/item/{name}", response_model=schemas.Item)
def create_item(name: str, item_base: schemas.ItemBase, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_name=name)
    if db_item is not None:
        raise HTTPException(status_code=404, detail="Item already exist")
    new_item= schemas.ItemCreate(name=name, **item_base.dict())
    return crud.create_item(db=db, item=new_item)

@app.delete("/item/{name}", response_model=schemas.Item)
def delete_item(name: str, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_name=name)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items", response_model=List[schemas.Item])
async def get_items(db: Session = Depends(get_db)):
    db_items = crud.get_items(db)
    return db_items