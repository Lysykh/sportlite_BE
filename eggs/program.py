from eggs.distance import sorted_plan, train

programm_run = train('run', 'pano', 5, 30) 
programm_bike = train('bike', 'pano', 5, 30) 
programm_swim = train('swimm', 'pano', 5, 30) 


sorted_plan_run = sorted(programm_run, key=lambda x: x['training_dif'])
sorted_plan_bike = sorted(programm_bike, key=lambda x: x['training_dif'])
sorted_plan_swim = sorted(programm_swim, key=lambda x: x['training_dif'])


second_training = sorted_plan[1]
print(second_training)

second_training = sorted_plan[1]
distance = second_training['work_distance_total']
print(f"Дистанция второй тренировки: {distance}")
r=0
programm_index = 0
# счетчик количества тренировок которые будет выдавать система в виде месячной программы. В целом можно сделать чтобы она выдавала программу и больше чем на месяц так как рассситываемых уровней разных тренировок с большим запасом
while programm_index <=20:
    

    
    print(f"Тренировка ПО БЕГУ {r}, {sorted_plan_run[programm_index]['training_number']}:")
    print(f"  Общая дистанция: {sorted_plan_run[programm_index]['work_distance_total']} метров")
    print(f"  Количество подходов: {sorted_plan_run[programm_index]['num_sets']}")
    print(f"  Количество повторений: {sorted_plan_run[programm_index]['num_reps']}")
    print(f"  Дистанция подхода: {sorted_plan_run[programm_index]['work_disatance']} метров")
    print(f"  Дистанция отдыха: {sorted_plan_run[programm_index]['light']} метров")
    print(f"  Темп бега: {sorted_plan_run[programm_index]['temp']} мин/км")
    print()
    r=r+1

    print(f"Тренировка ПО ВЕЛОСИПЕДУ {r}, {sorted_plan_bike[programm_index]['training_number']}:")
    print(f"  Общая дистанция: {sorted_plan_bike[programm_index]['work_distance_total']} метров")
    print(f"  Количество подходов: {sorted_plan_bike[programm_index]['num_sets']}")
    print(f"  Количество повторений: {sorted_plan_bike[programm_index]['num_reps']}")
    print(f"  Дистанция подхода: {sorted_plan_bike[programm_index]['work_disatance']} метров")
    print(f"  Дистанция отдыха: {sorted_plan_bike[programm_index]['light']} метров")
    print(f"  Темп бега: {sorted_plan_bike[programm_index]['temp']} мин/км")
    print()
    r=r+1

    print(f"Тренировка ПО ПЛАВАНИ {r}, {sorted_plan_swim[programm_index]['training_number']}:")
    print(f"  Общая дистанция: {sorted_plan_swim[programm_index]['work_distance_total']} метров")
    print(f"  Количество подходов: {sorted_plan_swim[programm_index]['num_sets']}")
    print(f"  Количество повторений: {sorted_plan_swim[programm_index]['num_reps']}")
    print(f"  Дистанция подхода: {sorted_plan_swim[programm_index]['work_disatance']} метров")
    print(f"  Дистанция отдыха: {sorted_plan_swim[programm_index]['light']} метров")
    print(f"  Темп бега: {sorted_plan_swim[programm_index]['temp']} мин/км")
    print()
    r=r+1
    programm_index = programm_index + 1


