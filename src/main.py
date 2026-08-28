from fastapi import FastAPI , HTTPException 
from pydantic import BaseModel , Field
from database.database import  (insert_to_task , db_con ,get_task_from_db , get_all_tasks_from_db , update_task_db , delete_task_db)
from database.postdb import create_postdb


create_postdb()

print('---------')
res =  get_task_from_db(2)
print(res)
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

    res = get_all_tasks_from_db()
    data = []

    for row in res:

        dic = {'id':row[0],
               'title':row[1],
                'done':bool(row[2])}

        data.append(dic)

    return data

@app.get('/tasks/{id}',status_code=200)
async def get_task(id:int):

    res = get_task_from_db(id)

    if res == None:
        raise HTTPException(status_code=400,detail="Task not found")

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
        insert_to_task(item)


@app.put('/tasks/{id}')
async def update_task(id:int,update:Update):
    if id < 0:
        raise HTTPException(status_code=404,detail="Couldn't find ID")
    
    if update.done is None and update.title is None:
        raise HTTPException(status_code=400,detail="Couldn't update the task")
    else:
        update_task_db(id,update.title,update.done)

        return "Task updated"

@app.delete('/tasks/{id}',status_code=204)
async def delete_task(id:int):
    if id<0 :
        raise HTTPException(status_code=404,detail="Couldn't find ID")
    else:
        delete_task_db(id)
    
        return "No Content"
        

    