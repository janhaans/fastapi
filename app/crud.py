from sqlalchemy.orm import Session

import models, schemas


def get_item(db: Session, item_name: str):
    return db.query(models.Item).filter(models.Item.name == item_name).first()

def get_items(db: Session):
    return db.query(models.Item).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_name: str):
    db_item = db.query(models.Item).filter(models.Item.name == item_name).first()
    db.delete(db_item)
    db.commit()
    return db_item
