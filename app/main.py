from fastapi import FastAPI, HTTPException, Query, Request, Form
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import closing

from pydantic import BaseModel
from datetime import datetime

from psycopg2 import sql




app = FastAPI()


# первая функция которая выводит нашу надпись

@app.get("/")
async def root():
    return {"message": "Hello World"}

# коннектор к базе данных/ не понятно зачем я его делаю тут отдельно так как потом все время его дублирую в каждой функции так как переменная все равно работает только внутри фенкции и вообще не понятно как Ювикорн обрабатывапет код питона

conn = psycopg2.connect(
    dbname="comments",
    user="oleg",
    password="123",
    host="db",
    port=5432,
)

cur = conn.cursor(cursor_factory=RealDictCursor)

# ==========
# # ДОМАШНЯЯ РАБОТА ИЗМЕНЕНИЕ ПОЛЬЗОВАТЕЛЯ
# # 3) Метод изменяющий пользователя пользователтя (PUT). 
# @app.put("/zamena/{item_id}")
# async def update_item(
#     item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
#     q: str | None = None,
#     item: Item | None = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     if item:
#         results.update({"item": item})
#     return results


class Item(BaseModel):
    name: str
    age: int
@app.put("/zamena/{item_id}")
def update_user(item_id: int, item: Item):
    # item.name = 'oleg'
    # item.age = 1
    cur.execute("UPDATE users SET name = %s, age = %s WHERE id = %s",(item.name, item.age, item_id))
    # response = cur.fetchone()
    # print(response)
    conn.commit()
    return {"message": f"Пользователь с ID {item_id} был успешно обновлен."}  

# ===== КОНЕЦ ДОМАШНЕЦ РАБОТЫ 

# ДОМАШЕНЕЕ ЗАДАНИЕ DELETE 



@app.delete("/delete_user/{item_id}")
def delete_user(item_id: int):

    cur.execute("DELETE FROM users WHERE id = %s", (item_id,))
    conn.commit()  
    return {"message": f"Пользователь с ID {item_id} был успешно удалён.",
            'response': response}


# КОНЕЦ ДОМАШНЕГО ЗАДАНИЯ DELETE


# === ДОМАШНЕЕ ЗАДАНИЕ №1 ===
# Выводит из базы данных пользователя по ID (fetchAll или fetchOne) #TODO:


@app.get("/take_user/{item_id}")
async def read_item(item_id: int):
    # async def read_item(item_id): - можно было и так написать, но int - типизирует данные и говорит что это обязательно число. Дима сказал что это неебаться как важно! 
    """Данная ручка возвращает данные пользователяв виде {
    "id": 2,
    "name": "John",
    "age": 3,
    "created_at": "2025-02-01T15:39:42.216806"
    }"""
    cur.execute("SELECT * FROM users WHERE id = %s", (item_id,))
    rows = cur.fetchone()
    return rows


# === ДОМАШНЕЕ ЗАДАНИЕ №2 ===
# Засовывает в базу данных пользователя методом POST

# Модель данных для POST-запроса
class Item(BaseModel):
    name: str
    age: int
@app.post("/insert/")
async def create_item(item: Item):
    # item.name='oleg'
    # item.age=32
    # print(item)
    cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)",(item.name, item.age),)
    # Сохраняем изменения
    conn.commit()
    return {"message": "Данные успешно добавлены", "item": item}





# # Забирае из базы данных методол GET первого пользователя
# @app.get("/first-user")
# async def get_first_user():
#     with closing(psycopg2.connect(
#             dbname="comments",
#             user="oleg",
#             password="123",
#             host="localhost",
#             port=5432,
#         )) as conn:
#         with closing(conn.cursor(cursor_factory=RealDictCursor)) as cur:
#             cur.execute("SELECT * FROM users LIMIT 1")
#             row = cur.fetchone()
#             print (row)
    
#     if row:
#         return {"user": row}
        
#     else:
#         return {"message": "No users found in the database."}




# # Засовывает пользователя в азу данных из формы
# app.mount("/static", StaticFiles(directory="static"), name="static")
# @app.post("/post_insert_form")
# async def create_user(request: Request):
#     form_data = await request.form()
#     name = form_data.get('name')
#     age = form_data.get('age')
    
#     # Запись данных в таблицу
#     cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
#     conn.commit()
    
#     return {"message": f"User {name} with age {age} was successfully added."}
# # ==КОНЕЦ работающий код для вставки из формы
 

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