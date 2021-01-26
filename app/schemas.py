from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    price: float
    quantity: Optional[int] = 0


class ItemCreate(ItemBase):
    name: str


class Item(ItemCreate):
    id: int

    class Config:
        orm_mode = True
