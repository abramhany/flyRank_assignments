from fastapi import FastAPI , HTTPException 
from pydantic import BaseModel , Field

from database.postdb import create_postdb , get_all_tasks , get_task_postgres, insert_task ,update_task_postgres , delete_task_postgres


create_postdb()


class Item(BaseModel):
    title:str = Field(min_length=1, strip_whitespace=True)

class Update(BaseModel):
    title:str = Field(min_length=1, strip_whitespace=True)
    done:bool 
    

app = FastAPI()

@app.get("/",status_code=201)
async def info():
    return {'name':"Task API",'version':"1.0","endpoints":['/tasks']}

@app.get('/health')
async def status():
    return {'status':"ok"}

@app.get("/tasks",status_code=200)
async def get_all():

    res = get_all_tasks()
    data = []

    for row in res:

        dic = {'id':row[0],
               'title':row[1],
                'done':bool(row[2])}

        data.append(dic)

    return data

@app.get('/tasks/{id}',status_code=200)
async def get_task(id:int):

    res = get_task_postgres(id)

    if res == None:
        raise HTTPException(status_code=404,detail="Task not found")

    else:

        dic = {
                    'id':id,
                    "title":res[1],
                    "done":bool(res[2])
                }
        
        return dic

@app.post('/tasks',status_code=201)
async def create_task(item:Item):
    if item.title.strip() == '':
        raise HTTPException(status_code=400,detail="Bad request")
    else:    
        res = insert_task(item.title)
        return res



@app.put('/tasks/{id}')
async def update_task(id:int,update:Update):
    if id < 0:
        raise HTTPException(status_code=404,detail="Couldn't find ID")
    
    if update.done is None and update.title is None:
        raise HTTPException(status_code=400,detail="Couldn't update the task")
    else:
        res = update_task_postgres(id,update.title,update.done)

        return res,"Task updated"

@app.delete('/tasks/{id}',status_code=204)
async def delete_task(id:int):
    if id<0 :
        raise HTTPException(status_code=404,detail="Couldn't find ID")
    else:
        res =delete_task_postgres(id)
        return f"{res} was deleted"
        

    