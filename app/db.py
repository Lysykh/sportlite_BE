#здесь мы будем подключаться к базе данных и потом забрать конкретную сессию
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base


from app.config import settings
# from app.models import Item

# все тут нужно включить из конфига а не вводить хардКодом
# сделать localhost переменной
DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@db/{settings.POSTGRES_DB}" #TODO заменить db на переменную из настроек
# это то же самое что и conn ектор
engine = create_async_engine(DATABASE_URL, future=True, echo=True)


# это то же самое что и cnnection& это одна из сессия так создается
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    future=True
)

# Base class for declarative models
# родитель всех таблиц 
Base = declarative_base()

# Dependency to get a database session
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

# в метадате лежит информация о всех наследниках base. ноо их само находит и делает то что мы просим
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  


