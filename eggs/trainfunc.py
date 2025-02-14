def generate_training_plan(initial_distance, speed1, speed2, num_trainings):
    training_plan = []
    current_distance = initial_distance

    for i in range(num_trainings):
        # Рассчитываем количество подходов и повторений
        num_sets = (i + 1)  # Количество подходов увеличивается с каждой тренировкой
        num_reps = (i + 1)  # Количество повторений увеличивается с каждой тренировкой

        # Рассчитываем дистанцию для каждого подхода
        set_distance = current_distance / num_sets

        # Создаем тренировку
        training = {
            'training_number': i + 1,
            'total_distance': current_distance,
            'num_sets': num_sets,
            'num_reps': num_reps,
            'set_distance': set_distance,
            'speed1': speed1,
            'speed2': speed2
        }

        training_plan.append(training)

        # Увеличиваем дистанцию для следующей тренировки
        current_distance += initial_distance * 0.1  # Увеличиваем на 10%

    return training_plan

# Параметры
initial_distance = 150  # Начальная дистанция (100 метров + 50 метров)
speed1 = 7  # Скорость для первой части (7 км/ч)
speed2 = 5  # Скорость для второй части (5 км/ч)
num_trainings = 40  # Количество тренировок

# Генерация плана тренировок
training_plan = generate_training_plan(initial_distance, speed1, speed2, num_trainings)

# Вывод плана тренировок
for training in training_plan:
    print(f"Тренировка {training['training_number']}:")
    print(f"  Общая дистанция: {training['total_distance']} метров")
    print(f"  Количество подходов: {training['num_sets']}")
    print(f"  Количество повторений: {training['num_reps']}")
    print(f"  Дистанция подхода: {training['set_distance']} метров")
    print(f"  Скорость 1: {training['speed1']} км/ч")
    print(f"  Скорость 2: {training['speed2']} км/ч")
    print()