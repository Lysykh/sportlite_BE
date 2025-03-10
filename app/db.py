#здесь мы будем подключаться к базе данных и потом забрать конкретную сессию


from app.config import settings

# все тут нужно включить из конфига а не вводить хардКодом
# сделать localhost переменной
DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@localhost/{settings.POSTGRES_DB}"

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
Base = declarative_base()

# Dependency to get a database session
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

