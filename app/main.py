from fastapi import FastAPI, Path, HTTPException, Depends
from pydantic import BaseModel
from typing import List

app = FastAPI()

items_by_name = {}

class ItemIn(BaseModel):
    price: float
    quantity: int

class ItemOut(ItemIn):
    name: str


def verify_item_not_in_db(name: str):
    item = items_by_name.get(name)
    if item is None:
        raise HTTPException(status_code=404, detail=f'Item {name} is not in the database')

def verify_item_in_db(name: str):
    item = items_by_name.get(name)
    if item is not None:
        raise HTTPException(status_code=404, detail=f'Item {name} is in the database')

def save_item_in_db(name: str, item: ItemIn):
    items_by_name[name] = { 'name': name, **item.dict() }
    return items_by_name.get(name)

@app.get("/item/{name}", response_model=ItemOut, dependencies=[Depends(verify_item_not_in_db)])
async def get_item(name: str):
    item = items_by_name.get(name)
    return item
    
@app.post("/item/{name}", response_model=ItemOut, dependencies=[Depends(verify_item_in_db)])
async def post_item(name: str, item: ItemIn):
    saved_item = save_item_in_db(name, item)
    return saved_item

@app.delete("/item/{name}", response_model=ItemOut, dependencies=[Depends(verify_item_not_in_db)])
async def delete_item(name: str):
    deleted_item = items_by_name.pop(name)
    return deleted_item

@app.get("/items", response_model=List[ItemOut])
async def get_items():
    items = [item for item in items_by_name.values()]
    return items

