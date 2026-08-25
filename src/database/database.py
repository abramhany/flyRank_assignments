import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()


db_location = os.getenv("DATABASE_LOCATION")


task_table = '''CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY,
  title TEXT,
  done BOOLEAN DEFAULT FALSE
);'''


async def create_database(db_location):
    con = sqlite3.connect(db_location)
    cur = con.cursor()
    cur.execute(task_table)
    res = cur.execute("SELECT name FROM sqlite_master")
    print(f"database tables: {res.fetchall()}")

def db_con():
    if not os.path.exists(db_location):
        create_database(db_location)

    else:

        con = sqlite3.connect(db_location)

        return con

def insert_to_task(title):
    data = (title,)
    con = db_con()
    cur = con.cursor()
    cur.execute(f"INSERT INTO tasks (title) VALUES (?)",data)
    con.commit()
    con.close()
    
    
def get_task_from_db(id:int):

    data = (id,)
    con = db_con()
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM tasks WHERE id=? ",data)
    res = res.fetchone()
    con.close()
    return res

def get_all_tasks_from_db():
    con = db_con()
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM tasks")
    res = res.fetchall()
    con.close()
    return res

def update_task(id:int,title:str,done:bool):
    data=(id,title,done)
    con = db_con()
    cur = con.cursor()
    cur.execute("UPDATE tasks SET title= ?,done= ?, WHERE id=?",data)
    con.commit()
    con.close()
        