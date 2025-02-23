from fastapi import FastAPI, Depends, Request, Query
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Функция для создания соединения с БД
def get_db_connection():
    connection = psycopg2.connect(
        dbname="comments",
        user="oleg",
        password="123",
        host="localhost",
        port=5432,
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    try:
        yield cursor
    finally:
        cursor.close()
        connection.close()


class User(BaseModel):
    name: str
    age: int


@app.get("/user")
async def create_user(name: str = Query(..., min_length=3), age: int = Query(..., gt=0), cursor=Depends(get_db_connection)):
    # Параметризация запроса для защиты от SQL-инъекций
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    return {"message": f"User {name} with age {age} was successfully added."}


@app.post("/user")
async def create_user_from_body(user: User, cursor=Depends(get_db_connection)):
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (user.name, user.age))
    return {"message": f"User {user.name} with age {user.age} was successfully added."}