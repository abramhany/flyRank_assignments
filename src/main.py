from fastapi import FastAPI , HTTPException 
from pydantic import BaseModel , Field


class Item(BaseModel):
    title:str = Field(min_length=1, strip_whitespace=True)

class Update(BaseModel):
    title:str | None = None
    done:bool | None = None
    

app = FastAPI()

@app.get("/",status_code=201)
async def info():
    return {'name':"Task API",'version':"1.0","endpoints":['/tasks']}
items = [
    {'id':0,"title":'test',"done":True},
    {'id':1,"title":'train',"done":False}
,]

@app.get('/health')
async def status():
    return {'status':"ok"}

@app.get("/tasks",status_code=200)
async def get_all():
    return items[:]

@app.get('/tasks/{id}',status_code=200)
async def get_task(id:int):
    if id > len(items):
        raise HTTPException(status_code=400,detail=f"Task {id} not found")
    return 200 ,items[id]

@app.post('/tasks',status_code=200)
async def create_task(item:Item):
    if item.title.strip() == '':
        raise HTTPException(status_code=400,detail="Bad request")
        

    id = len(items)
    dic = {
        'id':id,
        "title":item.title,
        "done":False
    }
    items.append(dic)
    print(id)
    return 201,items[id]

@app.put('/tasks/{id}')
async def update_task(id:int,update:Update):
    if id > len(items):
        raise HTTPException(status_code=404,detail="Couldn't find ID")
    
    if update.done is None and update.title is None:
        raise HTTPException(status_code=400,detail="Couldn't update the task")

    dic = items[id]

    if update.done is not None:
        dic['done'] = update.done

    if update.title is not None:
        dic['title'] = update.title

    return items[id]

@app.delete('/tasks/{id}',status_code=204)
async def update_task(id:int):
    if id<0 or id > len(items):
        raise HTTPException(status_code=404,detail="Couldn't find ID")
    
    del items[id]

    return "No Content"
        

    