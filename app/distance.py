
# # todo
# 1. должны быть нормальные округленные метры ++
# 2. дистанции должны быть подготовленны под стандартный манеж и стандартный бассейн ++
# 3. добавить время и остальные атрибуты 
# 4. сделать календарь для бега плавания и велика отдельно и триатлонный вместе возможно какой то алгоритм чтобы он был уникальный ++
# 5. сделать какое-то понятное сохранение чтобы было монетно тяжело тебе было или нет
# 6. сделать кнопку логики снижения нагрузки. За счет увеличения отыха. При этом необходимо сохранить пропорции дистанции для стандартных кругов
# 7. подумать над логикой лесенок или возрастающей негрузк или частично нагрузки их разных зон что-то вроед комплексных тренировок
# 8. подумать логику и описание под разные дистанции и задачи и кстати доделать это в дизайне типа под похудение может быть добавить калории
# 9. может быть какие-то рекомендации 

# функция расчета тренировок переменные 
# НАБОР ПЕРЕМЕННЫХ ДЛЯ РАСЧЕТА РАБОЧИХ ДИСТАНЦИЙ
# work_distance_total - общая дистанция тренировки которая складывается из дистанции умноженной на повторения и подходы
# work_distance_min - минимальная дистанция работы
# work_distance_max - максимальная дистанция работы 
# work_distance_step - шаг с которым растет дистанция work_distance между work_distance_min и work_distance_max 
# work_distance - расчетная величина между  work_distance_min и work_distance_max это дистанция каждого повтора и она должна увеличиваться с ростом нагрузки по +100м 

# НАБОР ПЕРЕМЕННЫХ ДЛЯ РАСЧЕТА ДИСТАНЦИЙ ОТДЫХА
# light_distance - дистанция отдыха расчетная веиличина от work_distance * light_distance_percent
# light_percent - какой процент составляет light_distance от work_distance. В Свою очередь этот показатель будет зависеть от того какой тип тренировки выбран Кардио Пано или МПК

# НАБОР ПЕРЕМЕННЫХ ДЛЯ РАСЧЕТА ТЕМПА
# initial_temp - задается пользователем. Темп pano. 
# temp_relax - коэффициент для отдыха
# temp_cardio - коэффициент для кардио тренировок
# temp_subpano - коэффициент для тренировок суб Пано
# temp_underpano - коэффициент для тренировок выше ПАно
# temp_mpk - - коэффициент для тренировок МПК

 
# num_level - количество тренировок в группе предварительно 40 
# level - уровень от 1 до num_level это тот уровень который выбирает пользователь
# rep_number - количество повторений
# sets_number - количество подходов
# dif_percent - коэффициент сложности 
# work_type - тип работы с утсановленными значениями mpl / pano / cardio
# sport - выбираемый вид спорта

# Счетчики 
# total_count - сквозной счетчик сидит внутри всех циклов и не прерывается
# sets_count - счетчик подходов - думаю не больше 4
# rep_count - счетчик вопвторов - до 10


def train(sport, work_type, pano_min, pano_sek):
    from aggs.temp_watt_zone import run_temp, swimm_temp, bike_temp
    from datetime import timedelta

    # Исходное время
    temp_pano = timedelta(minutes=pano_min, seconds=pano_sek)

    if sport == 'run':
        work_distence_step = 200
        temp = run_temp
        if work_type == 'mpk':
            work_distance_min = 200 
            work_distance_max = 600
        if work_type == 'pano':            
            work_distance_min = 400
            work_distance_max = 1000
        if work_type == 'cardio':           
            work_distance_min = 400 
            work_distance_max = 2000    

    if sport == 'swimm':
        temp = swimm_temp
        work_distence_step = 50
        if work_type == 'mpk':            
            work_distance_min = 50 
            work_distance_max = 400
        if work_type == 'pano':            
            work_distance_min = 100
            work_distance_max = 600
        if work_type == 'cardio':            
            work_distance_min = 400 
            work_distance_max = 1000
    
    if sport == 'bike':
        work_distence_step = 2000
        temp = bike_temp
        if work_type == 'mpk':           
            work_distance_min = 2000 
            work_distance_max = 6000
        if work_type == 'pano': 
            work_distance_min = 4000
            work_distance_max = 10000            
        if work_type == 'cardio':
            work_distance_min = 4000 
            work_distance_max = 20000   
             


    training_plan=[]
    
    work_distance_total = work_distance_min
    sets_count = 1
    total_count = 1
    rep_count = 1

    while sets_count <= 2: 
        print('большой цикл до')
        rep_count = 1
        while rep_count <= 10:
            work_distance = work_distance_min
            dif_percent_count2 = 0.8
            while work_distance <= work_distance_max:
                if sport == 'swimm':
                    if work_type == 'mpk':
                        light_distance = 100  
                    if work_type == 'pano': 
                        light_distance = 50
                    if work_type == 'cardio':
                        light_distance = 25  
                else:
                    if work_type == 'mpk':
                        light_distance = work_distance  
                    if work_type == 'pano': 
                        light_distance = work_distance / 2
                    if work_type == 'cardio':
                        light_distance = work_distance / 4                                          
                
                work_distance_total = (work_distance + light_distance) * rep_count * sets_count
                if sets_count == 1: 
                    dif_percent_count = 1
                if sets_count == 2: 
                    dif_percent_count = 0.9                  
                                         
                dif_percent = work_distance_total * dif_percent_count * dif_percent_count2
                dif_percent_count2 = dif_percent_count2 + 0.01
                    # Создаем тренировку
                training = {
                    'training_dif': dif_percent,
                    'training_number': total_count,
                    'work_distance_total': work_distance_total,
                    'num_sets': sets_count,
                    'num_reps': rep_count,
                    'work_disatance': work_distance,
                    'light': light_distance,
                    'temp': temp_pano * temp[work_type],
                    
                }
                training_plan.append(training)

                print(work_distance)
                
                work_distance = work_distance + work_distence_step
                total_count = total_count + 1  
                print(work_distance_total)
                print(rep_count)
                print(sets_count)
                print(total_count)
                print('внутри')
                print(work_distance)
            rep_count = rep_count + 1
        print('большой цикл после')
        sets_count = sets_count + 1
    return training_plan

plan = train('run','pano',5,30,)

# # Использование break для прерывания цикла
# for i in range(10):
#     if i == 5:
#         break
#     print(i)

# # Сортируем тренировки по общей дистанции в порядке возрастания
# sorted_plan = sorted(plan, key=lambda x: x['total_distance'])
# Сортируем тренировки по общей дистанции в порядке убывания



sorted_plan = sorted(plan, key=lambda x: x['training_dif'])

r=1

for training in sorted_plan:
    print(f"Тренировка {r}, {training['training_dif']}:")
    print(f"Тренировка {r}, {training['training_number']}:")
    print(f"  Общая дистанция: {training['work_distance_total']} метров")
    print(f"  Количество подходов: {training['num_sets']}")
    print(f"  Количество повторений: {training['num_reps']}")
    print(f"  Дистанция подхода: {training['work_disatance']} метров")
    print(f"  Дистанция отдыха: {training['light']} метров")
    print(f"  Темп бега: {training['temp']} мин/км")
    print()
    if r == 40:
        break
    r=r+1


