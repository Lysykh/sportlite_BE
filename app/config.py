#здесь мы будем забирать переменные из .env и работать с остальными переменными окружения программы Это делается с помощью pydentic settings 
# https://docs.pydantic.dev/latest/concepts/pydantic_settings/

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
#TODO дописать переменную модел кофиг так так чтобы путь к env был в явном виде

# POSTGRES_PASSWORD=123
# POSTGRES_USER=oleg
# POSTGRES_DB=comments

settings = Settings()


if __name__ == "__main__":
    print(settings)


мы на алхимии