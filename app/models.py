# здесь мы будем описывать струтктуру таблиц базы данных используя SQL Алхимию 
# https://docs.sqlalchemy.org/en/20/
from sqlalchemy import Column, Integer, String
from app.db import Base
class ItemCreate(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(String)
