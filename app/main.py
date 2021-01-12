from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ItemModel(BaseModel):
    name: str
    price: float
    quantity: int

@app.get("/")
async def root():
    return {'message': 'Hello World!'}

@app.get("/item/{item_id}")
async def get_item(item_id: int, item: ItemModel):
    item_dict = item.dict()
    response = { "item_id": item_id }
    response.update(item_dict)
    return response
