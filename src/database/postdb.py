import psycopg
from dotenv import load_dotenv
import os

load_dotenv()


db_location = os.getenv("DATABASE_URL")


table_schema = """
CREATE TABLE IF NOT EXISTS tasks (
  id SERIAL PRIMARY KEY,
  title TEXT,
  done BOOLEAN DEFAULT FALSE
);"""

def create_postdb():
    with psycopg.connect(db_location) as con:
        with con.cursor() as cur:
            cur.execute(table_schema)
            con.commit()

            cur.execute("SELECT * FROM tasks;")
            tasks = cur.fetchall()
            print(f"Existing tasks: {tasks}")
            
            if not tasks:
                cur.executemany(""" 
                         INSERT INTO tasks (title) VALUES (%s) RETURNING *;""",
                         [('learn to cook',),('learn to shoot',),('learn to follow the damn train cj',)],
                         returning=True)
                
                print(cur.fetchall())
          
                
            cur.execute("""
                SELECT tablename 
                FROM pg_catalog.pg_tables 
                WHERE schemaname='public';
            """)
            
            res = cur.fetchall()
            con.close()
            print(f"Database tables: {res}")


def get_all_tasks():
     with psycopg.connect(db_location) as con:
            with con.cursor() as cur:
              
              cur.execute("SELECT * FROM tasks;")
              con.commit()
              res = cur.fetchall()
              con.close()
              
              return res
def get_task_postgres(id):
     with psycopg.connect(db_location) as con:
                 with con.cursor() as cur:
                   
                  cur.execute("SELECT * FROM tasks WHERE id=%s;",(id,))
                  con.commit()
                  res = cur.fetchone()
                  con.close()

                  return res

def insert_task(title):
    with psycopg.connect(db_location) as con:
                with con.cursor() as cur:

                  cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING *;",(title,))
                  con.commit()
                  res = cur.fetchone()
                  con.close()

                  return res

def update_task_postgres(id,title,done):
      with psycopg.connect(db_location) as con:
                      with con.cursor() as cur:
                        cur.execute("UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING * ;",(title,done,id))
                        con.commit()
                        res = cur.fetchone()
                        con.close()

                        return res

def delete_task_postgres(id):
      with psycopg.connect(db_location) as con:
                      with con.cursor() as cur:
                        cur.execute("DELETE FROM tasks WHERE id =%s RETURNING *;",(id,))
                        con.commit()
                        res = cur.fetchone()
                        con.close()

                        return res