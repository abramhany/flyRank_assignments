from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def status():
    return {'Status':"Online"}
items = {
    1:"house",2:'mouse'
}
@app.get('/item/{id}')
def add_item(id:int):
    if id > len(items):
        return "not there"
    return items[id]