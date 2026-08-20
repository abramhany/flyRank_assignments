from fastapi import FastAPI
#from enum import Enum

app = FastAPI()

@app.get("/")
async def info():
    return {'name':"Task API",'version':"1.0","endpoints":['/item']}
items = {
    1:"house",2:'mouse'
}

@app.get('/health')
async def status():
    return {'status':"ok"}

@app.get("/item/all")
async def get_all():
    return items

@app.get('/item/{id}')
async def get_item(id:int):
    if id > len(items):
        return "not there"
    return items[id]

@app.post('/item/{name}')
async def create_item(item_name:str):
    id = len(items) +1
    items[id] = item_name
    return {id:items[id]}