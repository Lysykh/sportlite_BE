# здесь мы будем описывать все pydentic схемы нашего проекта 

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    age: int