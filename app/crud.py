
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import ItemCreate
from app.schemas import Item as ItemShema

# функция которая что-то в базу вставляет
async def isert_item(item: ItemShema, session: AsyncSession):    
    new_item = ItemCreate(name=item.name, age=item.age)
    session.add(new_item)
    await session.commit()





