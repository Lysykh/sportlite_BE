rec = {"message": f"User with age was successfully added."}
print (rec, type(rec))


from pydantic import BaseModel


class Item(BaseModel):
    name: str
    age: int

user=Item(name='Oleg', age=40)
print(user)  