from fastapi import FastAPI , HTTPException ,Depends
from pydantic import BaseModel , Field
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from supabase import Client, create_client , AuthWeakPasswordError , AuthApiError
from dotenv import load_dotenv
import os
from database.postdb import create_postdb , get_all_tasks , get_task_postgres, insert_task ,update_task_postgres , delete_task_postgres
from schema.database import Item , Update
from schema.auth import SignUp
load_dotenv()


oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth')
create_postdb()

supabase: Client = create_client(

    supabase_url=os.environ.get("SUPABASE_URL"),
   supabase_key=os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)

    

app = FastAPI()

@app.get("/",status_code=201)
async def info():
    return {'name':"Task API",'version':"1.0","endpoints":['/tasks']}


@app.post('/auth/signup',status_code=201)
async def signup(sign_up:SignUp):
    try :
        supabase.auth.sign_up({
            "email":sign_up.email,
            "password" : sign_up.password
        })
    except AuthWeakPasswordError :
        raise HTTPException(400,detail="Bad Request") 
    
    return "Created"

@app.post('/auth/login',status_code=201)
async def login(sign_up:SignUp):
    try :
        response = supabase.auth.sign_in_with_password({
            "email":sign_up.email,
            "password" : sign_up.password
        })
    except AuthApiError :
        raise HTTPException(400,detail="Invalid login credentials")
    
    return response.session.access_token

@app.get('/health')
async def status():
    return {'status':"ok"}

@app.get("/tasks",status_code=200)
async def get_all(token:Annotated[str,Depends(oauth2_schema)]):

    res = get_all_tasks()
    data = []

    for row in res:

        dic = {'id':row[0],
               'title':row[1],
                'done':bool(row[2])}

        data.append(dic)

    return data , token

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
        

    