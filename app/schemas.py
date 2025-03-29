# здесь мы будем описывать все pydentic схемы нашего проекта 

from pydantic import BaseModel

class Item(BaseModel):
    name: str 
    age: str

class New_user_pydentic_schemas(BaseModel):
    name: str 
    age: str

class Workout_pydentic_schemas(BaseModel):
    distance: str 
    time: str    

# class ItemCreate(BaseModel):
#     name: str
#     age: str

# class ItemResponse(BaseModel):
#     id: int

#     class Config:
#         from_attributes = True  


# shema1 = Item(name="oleg", age=2)

# if __name__ == "__main__":
#     print(shema1)

# print(shema1.age)