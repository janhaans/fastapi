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


@app.get("/item", response_model=schemas.Item)
def get_item(item: schemas.ItemRead, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, name=item.name)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.post("/item", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, name=item.name)
    if db_item is not None:
        raise HTTPException(status_code=404, detail="Item already exist")
    return crud.create_item(db, item)

@app.delete("/item", response_model=schemas.Item)
def delete_item(item: schemas.ItemRead, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, name=item.name)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items", response_model=List[schemas.Item])
def get_items(db: Session = Depends(get_db)):
    db_items = crud.get_items(db)
    return db_items

@app.get("/shop", response_model=schemas.Shop)
def get_shop(shop: schemas.ShopRead, db: Session = Depends(get_db)):
    db_shop = crud.get_shop(db, name=shop.name)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@app.post("/shop", response_model=schemas.Shop)
def create_shop(shop: schemas.ShopCreate, db: Session = Depends(get_db)):
    db_shop = crud.get_shop(db, name=shop.name)
    if db_shop is not None:
        raise HTTPException(status_code=404, detail="Shop already exist")
    return crud.create_shop(db, shop)

@app.delete("/shop", response_model=schemas.Shop)
def delete_shop(shop: schemas.ShopRead, db: Session = Depends(get_db)):
    db_shop = crud.delete_shop(db, name=shop.name)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@app.get("/shops", response_model=List[schemas.Shop])
def get_items(db: Session = Depends(get_db)):
    db_shops = crud.get_shops(db)
    return db_shops


@app.get("/stock", response_model=schemas.StockOutput)
def get_stock(stock: schemas.StockRead, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, name=stock.item_name)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_shop = crud.get_shop(db, name=stock.shop_name)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    db_stock = crud.get_stock(db, item_id=db_item.id, shop_id=db_shop.id)
    stock = schemas.StockOutput(item=db_item, shop=db_shop, quantity=db_stock.quantity)
    return stock

@app.post("/stock", response_model=schemas.Stock)
def create_stock(stock: schemas.StockCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, name=stock.item_name)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_shop = crud.get_shop(db, name=stock.shop_name)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    new_stock = schemas.StockDBIn(item_id=db_item.id, shop_id=db_shop.id, quantity=stock.quantity)
    return crud.create_stock(db=db, stock=new_stock)

