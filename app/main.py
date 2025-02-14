from fastapi import FastAPI, Query, Request, Form
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import closing

app = FastAPI()

# Указываем, где находятся статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")


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


@app.post("/user")
async def create_user(request: Request):
    form_data = await request.form()
    name = form_data.get('name')
    age = int(form_data.get('age'))
    
    # Запись данных в таблицу
    cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    
    return {"message": f"User {name} with age {age} was successfully added."}


@app.get("/first-user")
async def get_first_user():
    with closing(psycopg2.connect(
            dbname="comments",
            user="oleg",
            password="123",
            host="localhost",
            port=5432,
        )) as conn:
        with closing(conn.cursor(cursor_factory=RealDictCursor)) as cur:
            cur.execute("SELECT * FROM users LIMIT 1")
            row = cur.fetchone()
            print (row)
    
    if row:
        return {"user": row}
        
    else:
        return {"message": "No users found in the database."}


templates = Jinja2Templates(directory="templates")

@app.get("/users", response_class=HTMLResponse)
async def get_users(request: Request):
    with closing(psycopg2.connect(
            dbname="comments",
            user="oleg",
            password="123",
            host="localhost",
            port=5432,
        )) as conn:
        with closing(conn.cursor(cursor_factory=RealDictCursor)) as cur:
            cur.execute("SELECT * FROM users")
            rows = cur.fetchall()
    
    return templates.TemplateResponse("index.html", {"request": request, "users": rows})


templates = Jinja2Templates(directory="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {"request": request, "name": "World"}
    return templates.TemplateResponse("index.html", context)


# # === НАЧАЛО Работающая часть кода, которая позволяет занести в базу данных значения из браузерной строки по методу GET===
# @app.get("/user")
# async def create_user(name: str = Query(...), age: int = Query(...)):
#     # Запись данных в таблицу
#     cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
#     conn.commit()
    
#     return {"message": f"User {name} with age {age} was successfully added."}
# # === КОНЕЦ Работающая часть кода, которая позволяет занести в базу данных значения из браузерной строки по методу GET===


# @app.post("/user")
# async def create_user(name: str = Form(...), age: int = Form(...)):
#     # Запись данных в таблицу
#     cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
#     conn.commit()
    
#     return {"message": f"User {name} with age {age} was successfully added."}




# from pydantic import BaseModel


# class Item(BaseModel):
#     name: str
#     age: int


# @app.post("/user")
# def create_user_from_form(user:Item):
#     print(user.age)
#     return user

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