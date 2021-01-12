from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {'message': 'Hello World!'}

@app.get("/items/{item_id}")
async def get_item(item_id: int, name: str):
    return {"item_id": item_id, "name": name}
