from sqlalchemy.orm import Session

import models, schemas


def get_item(db: Session, name: str):
    return db.query(models.Item).filter(models.Item.name == name).first()

def get_items(db: Session):
    return db.query(models.Item).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, name: str):
    db_item = db.query(models.Item).filter(models.Item.name == name).first()
    db.delete(db_item)
    db.commit()
    return db_item

def get_shop(db: Session, name: str):
    return db.query(models.Shop).filter(models.Shop.name == name).first()

def get_shops(db: Session):
    return db.query(models.Shop).all()

def create_shop(db: Session, shop: schemas.ShopCreate):
    db_shop = models.Shop(**shop.dict())
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop

def delete_shop(db: Session, name: str):
    db_shop = db.query(models.Shop).filter(models.Shop.name == name).first()
    db.delete(db_shop)
    db.commit()
    return db_shop

def get_stock(db: Session, item_id: int, shop_id: int):
    return db.query(models.Stock).filter(models.Stock.item_id == item_id and models.Stock.shop_id == shop_id).first()

def create_stock(db: Session, stock: schemas.StockDBIn):
    db_stock = model.Stock(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock