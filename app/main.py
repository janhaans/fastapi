from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel

app = FastAPI()

items_by_name = {}

class Item(BaseModel):
    price: float
    quantity: int

@app.get("/")
async def root():
    return {'message': 'Hello World!'}

@app.get("/item/{name}")
async def get_item( name: str = Path(..., title="Item name") ):
    item = items_by_name.get(name)
    if item is None:
        raise HTTPException(status_code=404, detail=f'Item {name} is not in the database')
    return { **items_by_name[name] }
    

@app.post("/item/{name}")
async def post_item( *,
                 name: str = Path(..., title="Item name"), 
                 item: Item ):
    found_item = items_by_name.get(name)
    if found_item:
        raise HTTPException(status_code=400, detail=f'Item {name} is in the database')
    items_by_name[name] = { 'name': name, **item.dict() }
    return { 'message': f'Item {name} is successfully saved' }
