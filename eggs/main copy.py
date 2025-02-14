from fastapi import FastAPI, Query
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

conn = psycopg2.connect(
    dbname="comments",
    user="oleg",
    password="123",
    host="localhost",
    port=5432,
)

cur = conn.cursor(cursor_factory=RealDictCursor)

@app.get("/user")
async def create_user(name: str = Query(...), age: int = Query(...)):
    # Запись данных в таблицу
    cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    
    return {"message": f"User {name} with age {age} was successfully added."}

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    age: int


@app.post("/user")
def create_user_from_form():
    pass

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


   # модифицирую код за счет задания значений функции внутри кода

# @app.get("/user")
# def create_user(name, age):
#     # Запись данных в таблицу
#     cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
#     conn.commit()
    
#     return {"message": f"User {name} with age {age} was successfully added."}

# inDB=create_user('test23', 1111)