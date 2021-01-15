from fastapi import FastAPI, Path, HTTPException, Depends
from pydantic import BaseModel
from typing import List

app = FastAPI()

items_by_name = {}

class ItemIn(BaseModel):
    price: float
    quantity: int

class ItemInDb(ItemIn):
    name: str

class ItemOut(ItemInDb):
    pass

async def verify_item_not_in_db(name: str):
    item = items_by_name.get(name)
    if item is None:
        raise HTTPException(status_code=404, detail=f'Item {name} is not in the database')

async def verify_item_in_db(name: str):
    item = items_by_name.get(name)
    if item is not None:
        raise HTTPException(status_code=404, detail=f'Item {name} is in the database')

def save_item_in_db(name: str, item: ItemIn):
    item_in_db = ItemInDb(name=name, **item.dict()) 
    items_by_name[name] = { **item_in_db.dict() }
    return item_in_db

@app.get("/item/{name}", response_model=ItemOut, dependencies=[Depends(verify_item_not_in_db)])
async def get_item(name: str):
    return { **items_by_name[name] }
    

@app.post("/item/{name}", response_model=ItemOut, dependencies=[Depends(verify_item_in_db)])
async def post_item(name: str, item: ItemIn):
    return save_item_in_db(name, item)

@app.get("/items", response_model=List[ItemOut])
async def get_items():
    return [item for item in items_by_name.values()]

