from datetime import timedelta

# переменные спрота : swim run bike
sport = 'run'

# переменная пано - это время в минутах и секундах
pano_min = 5
pano_sec = 30

# Исходное время
initial_temp = timedelta(minutes=pano_min, seconds=pano_sec)

# расчет времени управжнения
cardio = initial_temp / 100 * 80
pano = initial_temp / 100 * 90
mpk = initial_temp / 100 * 110
speed = initial_temp / 100 * 120



# Прибавляем 10 секунд
added_time = initial_temp + timedelta(seconds=10)

# Делим время на 2
half_time = added_time / 2

# # Выводим результат
# print(f"После умножения на 80%: {cardio}")
# print(f"После прибавления 10 секунд: {added_time}")
# print(f"После деления на 2: {half_time}")

# Преобразуем результат в минуты и секунды для удобства
total_seconds = half_time.total_seconds()
minutes = int(total_seconds // 60)
seconds = int(total_seconds % 60)

# print(f"Результат: {minutes} минут {seconds} секунд")