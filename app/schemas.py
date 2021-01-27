from typing import List, Optional

from pydantic import BaseModel

class ItemRead(BaseModel):
    name: str

class ItemCreate(ItemRead):
    price: float

class Item(ItemCreate):
    id: int

    class Config:
        orm_mode = True


class ShopRead(BaseModel):
    name: str
    
class ShopCreate(ShopRead):    
    location: str

class Shop(ShopCreate):
    id: int

    class Config:
        orm_mode = True


class StockRead(BaseModel):
    item_name: str
    shop_name: str

class StockCreate(StockRead):
    quantity: int

class StockOutput(BaseModel):
    item: Item
    shop: Shop
    quantity: int

class StockDBIn(BaseModel):
    item_id: int
    shop_id: int
    quantity: int

class Stock(StockDBIn):
    id: int
    quantity: int

    class Config:
        orm_mode = True