from fastapi import FastAPI , status
from pydantic import BaseModel , Field


class Item(BaseModel):
    title:str = Field(min_length=1, strip_whitespace=True)


app = FastAPI()

@app.get("/")
async def info():
    return {'name':"Task API",'version':"1.0","endpoints":['/tasks']}
items = [
    {'id':0,"title":'test',"done":True},
    {'id':1,"title":'train',"done":False}
,]

@app.get('/health')
async def status():
    return {'status':"ok"}

@app.get("/task/all")
async def get_all():
    return items[:]

@app.get('/tasks/{id}',status_code=200)
async def get_item(id:int):
    if id > len(items):
        return 400,{"error": f"Task {id} not found"}
    return 200 ,items[id]

@app.post('/tasks/')
async def create_item(item:Item):
    if item.title.strip() == '':
        return 400,{'Error':"Bad Request"}

    
    id = len(items)

    dic = {
        'id':id,
        "title":item.title,
        "done":False
    }

    items.append(dic)
    print(id)
    return 201,items[id]