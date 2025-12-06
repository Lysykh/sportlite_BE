import asyncio
from fastapi import Depends, FastAPI, HTTPException, Query, Request, Form
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager, closing

from pydantic import BaseModel
from datetime import datetime

from psycopg2 import sql
from sqlalchemy import select
from app.config import settings
from app.models import ItemCreate, New_user, Workout
from app import models

import ssl


from sqlalchemy.ext.asyncio import AsyncSession
from app.db import create_tables, get_db
from app.schemas import Item, New_user_pydentic_schemas, Workout_pydentic_schemas, Create_user_email_pydentic_schemas

from sqlalchemy.orm import sessionmaker
from app.db import engine
from app.crud import isert_item, isert_in_new_user, isert_in_workout 
from app.crud import add_workout_to_user

from sqlalchemy import insert
from app.models import user_workout_association

from fastapi.middleware.cors import CORSMiddleware


async def lifespan(app: FastAPI):
    # Код, выполняемый при запуске приложения
    await create_tables()
    yield
    # Код, выполняемый при завершении работы приложения
    await engine.dispose()

# ТОЛЬКО ОДИН РАЗ СОЗДАЕМ ПРИЛОЖЕНИЕ!
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React development server
        "http://localhost:8081",  # React Native development server
        # Дополнительные адреса при необходимости
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/")
async def root():
    count = 0
    test2 = []
    while count < 10:   
        test = 1 + 2
        spisok = {
            'training_dif': count,
            'training_number': count,
        }
        test2.append(spisok)
        count = count + 1
    return {"message": "Hello World", "test": "some", "test2": test2}  
    

# СВЯЗЬ ТАБЛИЦ
@app.post("/users/{user_id}/add-workout/{workout_id}")
async def add_workout_to_user_handler(
    user_id: int,
    workout_id: int,
    session: AsyncSession = Depends(get_db)
):
    return await add_workout_to_user(user_id, workout_id, session)

@app.post("/create_user_email/")
async def create_user_email(
    item: Create_user_email_pydentic_schemas, 
    session: AsyncSession = Depends(get_db)
):
    new_item = await isert_in_new_user(item, session)
    return new_item

@app.post("/create/")
async def create_item_handler(
    item: Item, 
    session: AsyncSession = Depends(get_db)
):
    new_item = await isert_item(item, session)
    return new_item

@app.post("/create_new_user/")
async def create_new_user(
    item: New_user_pydentic_schemas, 
    session: AsyncSession = Depends(get_db)
):
    new_item = await isert_in_new_user(item, session)
    return new_item


@app.post("/create_workout/")
async def create_workout_handler(
    item: Workout_pydentic_schemas, 
    session: AsyncSession = Depends(get_db)
):
    new_item = await isert_in_workout(item, session)
    return new_item

@app.get("/get-items/{item_id}")
async def get_items(
    item_id: int, 
    session: AsyncSession = Depends(get_db)
):
    result = await session.execute(select(ItemCreate).where(ItemCreate.id == item_id))
    item = result.scalars().first()
    return item


@app.get("/get-user/{user_id}")
async def get_user(
    user_id: int, 
    session: AsyncSession = Depends(get_db)
):
    result = await session.execute(select(New_user).where(New_user.id == user_id))
    item = result.scalars().first()
    return item


@app.get("/get-programm/")
async def get_programm(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(ItemCreate))
    zabiraemizkursora = result.scalars().first()
    return zabiraemizkursora


@app.get("/get-items-pydentic/{item_id}", response_model=Item)
async def get_item2(
    item_id: int, 
    session: AsyncSession = Depends(get_db)
):
    result = await session.execute(select(ItemCreate).where(ItemCreate.id == item_id))
    item = result.scalars().first()
    return item


@app.post("/request_gigachat/")
async def request_gigachat(item: Create_user_email_pydentic_schemas):
    new_item = {}
    return new_item

# ФУНКЦИЯ КОНТАКТ С ГИГАЧАТОМ
@app.post("/request_gigachat2/{promt}")
async def request_gigachat2(promt: str):
    # Создаем кастомный SSL контекст без проверки сертификатов
    from gigachat import GigaChat
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    giga = GigaChat(
        credentials='MWIwYjY4ZjctYmQ1Ny00MDcyLWEzNWMtYzYwNWY4NTNjNjg5OmJmOWI3YmYyLThmNDAtNDFhMi05ZGI2LTI0ZmVmMTY4ZDY5MA==',
        verify_ssl_certs=False,
        ssl_context=ssl_context
    )

    response = giga.chat(promt)
    print(response.choices[0].message.content)
    answer = response.choices[0].message.content

    return answer

# @app.post("/items/", response_model=ItemResponse)
# async def create_item_handler(item: ItemCreate, session: AsyncSession = Depends(get_db)):
#     new_item = Item(name=item.name, age=item.age)  # Используйте SQLAlchemy модель
#     session.add(new_item)
#     await session.commit()
#     await session.refresh(new_item)
#     return new_item  # FastAPI автоматически сериализует new_item в ItemResponse

# коннектор к базе данных/ не понятно зачем я его делаю тут отдельно так как потом все время его дублирую в каждой функции так как переменная все равно работает только внутри фенкции и вообще не понятно как Ювикорн обрабатывапет код питона

# conn = psycopg2.connect(
#     dbname="comments",
#     user="oleg",
#     password = settings.POSTGRES_PASSWORD,
#     host="db",
#     port=5432,
# )

# cur = conn.cursor(cursor_factory=RealDictCursor)


# ДОМАШНЯЯ РАБОТА "СОЗДАНИЕ ТАБЛИЦЫ"
# Создаю функцию создания таблицы. Не понял где тут нужен класс. Точнее так как этот класс сюда присобавить. 
# Просто создал табличу с теми же полями/

# def create_items_table():
#     create_table_query = """
#     CREATE TABLE IF NOT EXISTS items (
#         id SERIAL PRIMARY KEY,
#         name VARCHAR(255) NOT NULL,
#         age INT NOT NULL
#     );
#     """
#     cur.execute(create_table_query)
#     conn.commit()
#     cur.close()
#     conn.close()
#     print("Таблица 'items' создана или уже существует.")

# # Создание таблицы при запуске приложения
# # Не понятно почему он его зачеркивает этот OnEvent
# @app.on_event("startup")
# def startup_event():
#     create_items_table()



# # ==========
# # # ДОМАШНЯЯ РАБОТА ИЗМЕНЕНИЕ ПОЛЬЗОВАТЕЛЯ
# # # 3) Метод изменяющий пользователя пользователтя (PUT). 
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


# # class Item(BaseModel):
# #     name: str
# #     age: int
# # @app.put("/zamena/{item_id}")
# # def update_user(item_id: int, item: Item):
# #     # item.name = 'oleg'
# #     # item.age = 1
# #     cur.execute("UPDATE users SET name = %s, age = %s WHERE id = %s",(item.name, item.age, item_id))
# #     # response = cur.fetchone()
# #     # print(response)
# #     conn.commit()
# #     return {"message": f"Пользователь с ID {item_id} был успешно обновлен."}  



# # ===== КОНЕЦ ДОМАШНЕЦ РАБОТЫ 

# # ДОМАШЕНЕЕ ЗАДАНИЕ DELETE 



# # @app.delete("/delete_user/{item_id}")
# # def delete_user(item_id: int):

# #     cur.execute("DELETE FROM users WHERE id = %s", (item_id,))
# #     conn.commit()  
# #     return {"message": f"Пользователь с ID {item_id} был успешно удалён.",
# #             'response': response}


# # КОНЕЦ ДОМАШНЕГО ЗАДАНИЯ DELETE


# # === ДОМАШНЕЕ ЗАДАНИЕ №1 ===
# # Выводит из базы данных пользователя по ID (fetchAll или fetchOne) #TODO:


# # @app.get("/take_user/{item_id}")
# # async def read_item(item_id: int):
# #     # async def read_item(item_id): - можно было и так написать, но int - типизирует данные и говорит что это обязательно число. Дима сказал что это неебаться как важно! 
# #     """Данная ручка возвращает данные пользователяв виде {
# #     "id": 2,
# #     "name": "John",
# #     "age": 3,
# #     "created_at": "2025-02-01T15:39:42.216806"
# #     }"""
# #     cur.execute("SELECT * FROM users WHERE id = %s", (item_id,))
# #     rows = cur.fetchone()
# #     return rows


# # === ДОМАШНЕЕ ЗАДАНИЕ №2 ===
# # Засовывает в базу данных пользователя методом POST

# # Модель данных для POST-запроса
# # class Item(BaseModel):
# #     name: str
# #     age: int
# # @app.post("/insert/")
# # async def create_item(item: Item):
# #     # item.name='oleg'
# #     # item.age=32
# #     # print(item)
# #     cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)",(item.name, item.age),)
# #     # Сохраняем изменения
# #     conn.commit()
# #     return {"message": "Данные успешно добавлены", "item": item}





# # # Забирае из базы данных методол GET первого пользователя
# # @app.get("/first-user")
# # async def get_first_user():
# #     with closing(psycopg2.connect(
# #             dbname="comments",
# #             user="oleg",
# #             password="123",
# #             host="localhost",
# #             port=5432,
# #         )) as conn:
# #         with closing(conn.cursor(cursor_factory=RealDictCursor)) as cur:
# #             cur.execute("SELECT * FROM users LIMIT 1")
# #             row = cur.fetchone()
# #             print (row)
    
# #     if row:
# #         return {"user": row}
        
# #     else:
# #         return {"message": "No users found in the database."}




# # # Засовывает пользователя в азу данных из формы
# # app.mount("/static", StaticFiles(directory="static"), name="static")
# # @app.post("/post_insert_form")
# # async def create_user(request: Request):
# #     form_data = await request.form()
# #     name = form_data.get('name')
# #     age = form_data.get('age')
    
# #     # Запись данных в таблицу
# #     cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
# #     conn.commit()
    
# #     return {"message": f"User {name} with age {age} was successfully added."}
# # # ==КОНЕЦ работающий код для вставки из формы
 

# # # === НАЧАЛО Работающая часть кода, которая позволяет занести в базу данных значения из браузерной строки по методу GET===
# # @app.get("/user")
# # async def create_user(name: str = Query(...), age: int = Query(...)):
# #     # Запись данных в таблицу
# #     cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
# #     conn.commit()
    
# #     retue": f"User {name} with age {age} was successfully added."}rn {"messag
# # # === КОНЕЦ Работающая часть кода, которая позволяет занести в базу данных значения из браузерной строки по методу GET===


# # @app.post("/user")
# # async def create_user(name: str = Form(...), age: int = Form(...)):
# #     # Запись данных в таблицу
# #     cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
# #     conn.commit()
    
# #     return {"message": f"User {name} with age {age} was successfully added."}




# # from pydantic import BaseModel


# # class Item(BaseModel):
# #     name: str
# #     age: int


# # @app.post("/user")
# # def create_user_from_form(user:Item):
# #     print(user.age)
# #     return user

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)


#    # модифицирую код за счет задания значений функции внутри кода

# # @app.get("/user")
# # def create_user(name, age):
# #     # Запись данных в таблицу
# #     cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
# #     conn.commit()
    
# #     return {"message": f"User {name} with age {age} was successfully added."}

# # inDB=create_user('test23', 1111)