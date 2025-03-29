# здесь мы будем описывать струтктуру таблиц базы данных используя SQL Алхимию 
# https://docs.sqlalchemy.org/en/20/
from sqlalchemy import Column, Integer, String
from app.db import Base

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class ItemCreate(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(String)


user_workout_association = Table(
    'user_workout_association',
    Base.metadata,
    Column('new_user_id', Integer, ForeignKey('new_user.id')),
    Column('workout_id', Integer, ForeignKey('workout.id'))
)

class New_user(Base):
    __tablename__ = "new_user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(String)

    # Связь 
    workouts = relationship(
        "Workout", 
        secondary=user_workout_association,
        back_populates="users"
    )

class Workout(Base):
    __tablename__ = "workout"

    id = Column(Integer, primary_key=True, index=True)
    distance = Column(String)
    time = Column(String)    

    # Связь 
    users = relationship(
        "New_user", 
        secondary=user_workout_association,
        back_populates="workouts"
    )

