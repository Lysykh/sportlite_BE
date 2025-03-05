#здесь мы будем забирать переменные из .env и работать с остальными переменными окружения программы Это делается с помощью pydentic settings 
# https://docs.pydantic.dev/latest/concepts/pydantic_settings/

import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Получаем значения из переменных окружения
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB")