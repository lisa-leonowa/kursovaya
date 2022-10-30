# подключение библиотек
from sympy import * # расчет корней уравнения
from numexpr import evaluate # рачет математического примера
from prettytable import PrettyTable


# превращает уравнение в математичкский пример
def create_ur(new_ur, znach):
    ur = new_ur.split('x')
    for i in range(len(ur)-1):
        ur[i] += f'({znach})'
    return ''.join(ur)


# находит недостающие промежутки
def for_table(num, sig, y, inc_dec):
    run = True
    i = 0
    while run:
        if inc_dec:
            new_num = num - i
        else:
            new_num = num + i
        if evaluate(create_ur(y, new_num)) > 0:
            sign = '+'
        else:
            sign = '-'
        if sign != sig:
            run = False
        else:
            i += 1
    return [new_num, sign]


# постароение таблицы для метода половинного деления
def clarification(a, b, y):
    # определение знаков на концах отрезка
    th = ['№', 'a', 'b', 'x = (a+b)/2', 'f(x)']
    if evaluate(create_ur(y, a)) > 0:
        s = '+'
    else:
        s = '-'
    th[1] += f'({s})'
    if evaluate(create_ur(y, b)) > 0:
        s = '+'
    else:
        s = '-'
    th[2] += f'({s})'

    # составление красивой таблицы
    table = PrettyTable(th)
    room = 0
    while (b-a)/(2**room) > 0.000001:
        x = (a + b) / 2
        f_x = evaluate(create_ur(y, x))
        a, b, x, f_x = round(a, 5), round(b, 5), round(x, 5), round(float(f_x), 5)

        table.add_row([room, a, b, x, f_x])
        if f_x > 0:
            s = '+'
        else:
            s = '-'
        if s in th[1]:
            a = x
        else:
            b = x
        room += 1

    f_x = evaluate(create_ur(y, x))
    a, b, x, f_x = round(a, 5), round(b, 5), round(x, 5), round(float(f_x), 5)
    table.add_row([room, a, b, x, f_x])
    return [table, x]


# метод половинного деления
def polov_del(mas_with_prom, y):
    print('Метод ПОЛОВИННОГО ДЕЛЕНИЯ')
    # вывод уточненных корней для каждого промежутка в таблице
    print('Определим корни уравнения на каждом промежутке:')
    floor = 1
    for i in mas_with_prom:
        print(f'Нахождение корня №{floor}')
        itog = clarification(i[0], i[1], y)
        print(itog[0])
        print(f'Корень №{floor} = {itog[1]} \n')
        floor += 1


# таблица для метода Хорд
def table_for_hord(mas, y, first_proiz, second_proiz):
    # определение знака второй производной
    # выбор нужной формулы для составления таблицы
    if float(evaluate(create_ur(y, mas[0]))) > 0:  # +-
        n = 0
        a_or_b = 1
    else:  # -+
        n = 1
        a_or_b = 0
    print(f'Начальная точка: {mas[n]}')

    resh = [float(evaluate(create_ur(str(first_proiz), mas[n]))), float(evaluate(create_ur(str(second_proiz), mas[n])))]
    if resh[0] * resh[1] > 0:
        th = ['№', 'Xn', 'f(Xn)', 'X(n+1) = Xn - ((f(Xn)*(Xn-a))/(f(Xn)-f(a)))', '|X(n+1)-Xn|']
    else:
        th = ['№', 'Xn', 'f(Xn)', 'X(n+1) = Xn - ((f(Xn)*(Xn-b))/(f(Xn)-f(b)))', '|X(n+1)-Xn|']
    table = PrettyTable(th)
    room = 0
    run = True
    while run:
        vr = th[-2][9::].split('f(Xn)')
        vr = f'({y})'.join(vr)
        vr = vr.split('Xn')
        vr = 'x'.join(vr)

        if 'f(a)' in vr:
            vr = vr.split('f(a)')
        elif 'f(b)' in vr:
            vr = vr.split('f(b)')
        f_a_or_b = create_ur(y, mas[a_or_b])
        vr = f'({f_a_or_b})'.join(vr)
        if 'a' in vr:
            vr = vr.split('a')
        elif 'b' in vr:
            vr = vr.split('b')
        vr = f'({mas[a_or_b]})'.join(vr)

        x_n = round(float(evaluate(create_ur(vr, mas[n]))), 5)
        table.add_row(
            [room, mas[n], round(float(evaluate(create_ur(y, mas[n]))), 5), x_n, abs(round((x_n - mas[n]), 5))])

        if abs(round((x_n - mas[n]), 5)) <= 0.00001:
            run = False

        room += 1
        mas[n] = x_n
    return table, mas[n]


# Уточнение промежутков для методов Хорд и Касательных
def utoch_prom(first_proiz, mas):
    mas_for_hord = [float(evaluate(create_ur(str(first_proiz), mas[0]))),
                    float(evaluate(create_ur(str(first_proiz), mas[1])))]
    M = max(abs(mas_for_hord[0]), abs(mas_for_hord[1]))
    m = min(abs(mas_for_hord[0]), abs(mas_for_hord[1]))
    while M >= (2 * m):
        x = (mas[0] + mas[1]) / 2
        if float(evaluate(create_ur(y, mas[0]))) > 0:
            if float(evaluate(create_ur(y, x))) > 0:
                mas[0] = x
            else:
                mas[1] = x
        else:
            if float(evaluate(create_ur(y, x))) < 0:
                mas[0] = x
            else:
                mas[1] = x

        mas_for_hord = [float(evaluate(create_ur(str(first_proiz), mas[0]))), float(evaluate(create_ur(str(first_proiz), mas[1])))]
        M = max(abs(mas_for_hord[0]), abs(mas_for_hord[1]))
        m = min(abs(mas_for_hord[0]), abs(mas_for_hord[1]))

    return mas


#метод Хорд
def hord(mas_with_prom, y):
    print('Метод ХОРД')

    # поиск первой и второй производных
    first_proiz = diff(y)
    print(f"f'(x) = {first_proiz}")

    second_proiz = diff(first_proiz)
    print(f"f''(x) = {second_proiz}")
    index = 1
    for mas in mas_with_prom:
        print(f'Запуск процесса нахождения корня №{index}')
        #нахожднение нужного промежутка
        mas = utoch_prom(first_proiz, mas)
        print(f'Нужный нам промежуток: ({mas[0]}; {mas[1]})')
        table, x_n = table_for_hord(mas, y, first_proiz, second_proiz)
        print(table)
        print(f'Корень №{index} будет: {x_n}\n')
        index += 1


# Таблица для метода Касательных
def table_for_kasat(mas, y, first_proiz, second_proiz):
    # определение знака второй производной
    # выбор нужной формулы для составления таблицы
    if float(evaluate(create_ur(y, mas[0]))) > 0:  # +-
        n = 1
        a_or_b = 0
    else:  # -+
        n = 0
        a_or_b = 1
    print(f'Начальная точка: {mas[n]}')

    # составление таблички
    th = ['№', 'Xn', 'f(Xn)', "X(n+1) = Xn - (f(Xn)/f'(Xn))", '|X(n+1)-Xn|']
    table = PrettyTable(th)
    room = 0

    # цикл добавлет строчки, пока разница между X и Xn не станеть меньше погрешности (0.00001)
    run = True
    while run:
        # преобразование формулы в матеатический пример
        vr = th[-2][9::].split("f'(Xn)")
        vr = f'({first_proiz})'.join(vr)
        vr = vr.split('f(Xn)')
        vr = f'({y})'.join(vr)
        vr = 'x'.join(vr.split('Xn'))

        # расчет нового X (Xn+1)
        x_n = round(float(evaluate(create_ur(vr, mas[n]))), 5)
        # добавление строки в таблиццу
        table.add_row([room, mas[n], round(float(evaluate(create_ur(y, mas[n]))), 5), x_n, abs(round((x_n - mas[n]), 5))])
        # проверка разница между X и Xn
        if abs(round((x_n - mas[n]), 5)) <= 0.00001:
            run = False
        # изменение Х
        mas[n] = x_n
        room += 1
    return table, mas[n]


# Метод Касательных
def kasat(mas_with_prom, y):
    print('Метод КАСАТЕЛЬНЫХ')

    # поиск первой и второй производных
    first_proiz = diff(y)
    print(f"f'(x) = {first_proiz}")

    second_proiz = diff(first_proiz)
    print(f"f''(x) = {second_proiz}")

    # поиск всех корней, index - переменная с номером корня
    index = 1
    for mas in mas_with_prom:
        # вызоы функции для уточнения промежутка
        mas = utoch_prom(first_proiz, mas)
        print(f'Промежуток для поиска корня №{index}: ({mas[0]}; {mas[1]})')
        print('Поиск корня начался ...')
        # вызов функции для составления таблицы
        table, x_n = table_for_kasat(mas, y, first_proiz, second_proiz)
        print(table)
        print(f'Корень №{index} = {x_n}\n')
        index += 1


# примеры линейных уравнений
y = input('Введите уравнение: ')# 10*x - 4 'x**3+3*x**2-3' 'x**4+2*x**3-x-3'
y1 = 'x**2+6*x-5'
y1 = '10*x**2-4'
y1 = 'x**3-12*x-8'
y1 = '7*x**4-3*x**3-6*x**2-4*x-8'
y1 = 'x**3-12*x-8'
print('Начинаем поиск корней для уравнения:', y)


# diff - считает производную от функции
print('Рассчитаем производную функции:', end=' ')
f_y = diff(y)
print(f_y)

# находим возможные корни уравнения
print('Найдем корни производной:', end=' ')
# solve - считает все реальные корни уравнения
# evaluate - считает значение математического примера
mas_otv = solve(f_y)

try:
    # поиск корней производной
    for i in range(len(mas_otv)):
        mas_otv[i] = evaluate(str(mas_otv[i]))
    korni_ur = mas_otv

    # вывод корней производной
    for i in mas_otv:
        print(i, end='; ')
    print()

    # сортировка возможных промежутков
    mas_otv.sort()

    # определение знаков в зависимости от значения
    mas = []
    new_mas = []
    for i in range(int(mas_otv[0]), int(mas_otv[-1])+1):
        new_mas.append(i)
        f_y = float(evaluate(create_ur(y, i)))
        if f_y > 0:
            mas.append('+')
        elif f_y < 0:
            mas.append('-')
        else:
            mas.append('?')
    mas_otv = new_mas

    # расчет недостающх значений для промежутков
    res = for_table(mas_otv[0], mas[0], y, True)
    mas_otv = [res[0]] + mas_otv
    mas = [res[1]] + mas

    res = for_table(mas_otv[-1], mas[-1], y, False)
    mas_otv = mas_otv + [res[0]]
    mas = mas + [res[1]]

    # вывод красивой таблички в консоль
    print('Расставим знаки функции и выведем в таблицу:')
    columns = len(mas_otv)
    table = PrettyTable(mas_otv)
    table.add_row(mas[:columns])
    print(table)

    # определение промежутков для возможных корней
    one = mas[0]
    mas_with_prom = []
    for i in range(len(mas)-1):
        if mas[i] != mas[i+1]:
            mas_with_prom.append([mas_otv[i], mas_otv[i+1]])

    # вывод промежутков, на которых лежат корни
    print('По таблице определяем, что корни уравнения лежат на прмежутках:')
    for i in mas_with_prom:
        print('(' + str(i[0]) + ', ' + str(i[1]) +')', end='; ')
    print('\n')

    # выбор нужного метода, отбражение ошибки неправильнного ввода
    check = True
    while check:
        number_ = input('Методы для вычисления:\n1) Метод Половинного деления\n2) Метод Хорд\n3) Метод Касательных (Ньютона)\nУкажите номер: ')

        if number_ == '1':
            polov_del(mas_with_prom, y) # метод половинного деления

        elif number_ == '2':
            hord(mas_with_prom, y) # метод хорд

        elif number_ == '3':
            kasat(mas_with_prom, y)

        else:
            print('Вы ввели некорректный номер! (Нужно 1, 2 или 3)')
except (ValueError, IndexError, SyntaxError) as e:
    print('Упс, не удалось рассчитать! Функция должна быть неприрывной!')
