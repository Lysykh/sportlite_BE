
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import ItemCreate, New_user, Workout

from app.schemas import Item as ItemShema
from app.schemas import New_user_pydentic_schemas
from app.schemas import Workout_pydentic_schemas
from sqlalchemy import insert
from app.models import user_workout_association

# фйнкция связи таблиц
async def add_workout_to_user(
    user_id: int,
    workout_id: int,
    session: AsyncSession
):

    # Явно добавляем запись в ассоциативную таблицу
    stmt = user_workout_association.insert().values(
        new_user_id=user_id,
        workout_id=workout_id
    )
    await session.execute(stmt)
    await session.commit()
    
    return {"message": "Workout added to user successfully"}

# функция которая что-то в базу вставляет
async def isert_item(item: ItemShema, session: AsyncSession):    
    new_item = ItemCreate(name=item.name, age=item.age)
    session.add(new_item)
    await session.commit()

async def isert_in_new_user(user: New_user_pydentic_schemas, session: AsyncSession):    
    New_user_c = New_user(name=user.name, age=user.age)
    session.add(New_user_c)
    await session.commit()

async def isert_in_workout(item: Workout_pydentic_schemas, session: AsyncSession):    
    new_workout = Workout(distance=item.distance, time=item.time)
    session.add(new_workout)
    await session.commit()





