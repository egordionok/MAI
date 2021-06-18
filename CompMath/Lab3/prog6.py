import tkinter as tk
import tkinter.font as tkFont
import math

def power_number(n_):
    if n_ == '0':
        return '\U00002070'
    elif n_ == '1':
        return '\U000000B9'
    elif n_ == '2':
        return '\U000000B2'
    elif n_ == '3':
        return '\U000000B3'
    elif n_ == '4':
        return '\U00002074'
    elif n_ == '5':
        return '\U00002075'
    elif n_ == '6':
        return '\U00002076'
    elif n_ == '7':
        return '\U00002077'
    elif n_ == '8':
        return '\U00002078'
    elif n_ == '9':
        return '\U00002079'

def power(__x):
    ans = ''
    __x = str(__x)
    for i in __x:
        ans += power_number(i)

    return ans

def print_polinom(coefs_, x='x'):
    if len(coefs_) == 1 and coefs_[0] == 0:
        return '0'
    polinom = ''
    n_ = len(coefs_)
    flag = True
    for coef in coefs_:
        n_ -= 1
        if coef == 0:
            continue
        if coef >= 0:
            if flag:
                flag = False
            else:
                polinom += '+'
        else:
            flag = False
            polinom += '-'

        if abs(coef) != 1 or n_ == 0:
            polinom += str(abs(coef))
        if n_ == 0:
            continue
        elif n_ == 1:
            polinom += x
        else:
            polinom += x + power(n_)

    polinom += '\n'
    return polinom

def Derivative(coefs__):
    coefs_  = [coefs__[i] for i in range(len(coefs__))]
    n = len(coefs_) - 1
    newcoefs_ = []
    for i in range(len(coefs_) - 1):
        newcoefs_.append(coefs_[i] * n)
        n -= 1

    if len(newcoefs_) == 0:
        newcoefs_.append(0)

    return newcoefs_

def Gorner(coefs_, x):
    ans = coefs_[0]
    for i in range(1, len(coefs_)):
        ans = coefs_[i] + x * ans

    return ans

def LowUpBounds(coefs__):
    coefs = [coefs__[i] for i in range(len(coefs__))]
    while coefs[len(coefs) - 1] == 0:
        coefs.pop()

    while coefs[0] == 0:
        coefs = coefs[1:]

    A = coefs[1]
    B = coefs[0]

    for i in range(len(coefs)):
        if abs(coefs[i]) > A and i != 0:                # max(|a1|, |a2|, ..., |a_n|)
            A = abs(coefs[i])
        if abs(coefs[i]) > B and i != len(coefs) - 1:   # max(|a0|, |a1|, ..., |a_n-1|)
            B = abs(coefs[i])

    return 1 / (1 + B / abs(coefs[len(coefs) - 1])), 1 + A / abs(coefs[0])  # r, R

def Division(divd__, divr__):
    divd = [divd__[i] for i in range(len(divd__))]
    divr = [divr__[i] for i in range(len(divr__))]
    divd_n = len(divd)
    divr_n = len(divr)
    result = [0 for i in range(divd_n)]

    for i in range(1, divr_n):
        divr[i] *= -1

    for i in range(divd_n - divr_n + 1):
        result[i] = divd[i] / divr[0]
        for j in range(1, divr_n):
            divd[i + j] += result[i] * divr[j]

    for i in range(divd_n - divr_n + 1, divd_n):
        result[i] = divd[i]

    res = [0 for i in range(divd_n - divr_n + 1)]
    res1 = [0 for i in range(divr_n - 1)]

    for i in range(divd_n):
        if i < divd_n - divr_n + 1:
            res[i] = result[i]
        else:
            res1[i - divd_n + divr_n - 1] = result[i]

    return res, res1

def Dichotomy(polinom, a, b):
    m = (a + b) / 2
    while math.fabs(Gorner(polinom, m)) >= 0.0001:
        m = (a + b) / 2
        a, b = (a, m) if Gorner(polinom, a) * Gorner(polinom, m) < 0 else (m, b)

    return (a + b) / 2

def Newton(coefs__):
    #   Подготовка полинома _______________________________
    coefs = [coefs__[i] for i in range(len(coefs__))]

    while coefs[len(coefs) - 1] == 0:
        coefs.pop()

    while coefs[0] == 0:
        coefs = coefs[1:]

    if coefs[0] < 0:
        for i in range(len(coefs)):
            coefs[i] = - coefs[i]
    #   Подготовка полинома _______________________________

    derivatives = []

    for i in range(len(coefs) - 1):     # Формируем масив производных
        derivatives.append(coefs)
        coefs = Derivative(coefs)

    c = 0
    while True:
        c += 1
        flag = True
        for coef in derivatives:
            if Gorner(coef, c) < 0:     # Проверяем знак производных в точке
                flag = False
                break

        if flag:
            break

    return c

def ShturmG(polinom__, a, b):
    polinom = [polinom__[i] for i in range(len(polinom__))]

    if polinom[0] < 0:
        for i in range(len(polinom)):
            polinom[i] *= -1

    shturm_system = []
    shturm_system.append(polinom)
    shturm_system.append(Derivative(polinom))

    n = 1
    while True:  # Формируем систему Штурма
        res, ost = Division(shturm_system[n - 1], shturm_system[n])
        for i in range(len(ost)):
            ost[i] *= -1

        if len(ost) == 0:
            break
        shturm_system.append(ost)
        n += 1

    Na = 0
    Nb = 0

    for i in range(0, len(shturm_system) - 1):  # Вычисляем число-во перемен знаков для границ
        if Gorner(shturm_system[i], a) * Gorner(shturm_system[i + 1], a) < 0:
            Na += 1
        if Gorner(shturm_system[i], b) * Gorner(shturm_system[i + 1], b) < 0:
            Nb += 1

    return Na - Nb

def HelpFunction(polinom, a, b):
    #   Вспомомгательная функция, которая помогает с помощью рекурсии отыскать интервал,
    #       на котором находится один корень

    intervals = []
    n = ShturmG(polinom, a, b)

    print(a, b, n)
    if n > 1:
        first = HelpFunction(polinom, (b + a) / 2, b)
        second = HelpFunction(polinom, a, (b + a) / 2)

        if len(first) > 0:
            if type(first[0]) == type(0):
                intervals.append(first)
            else:
                for i in first:
                    intervals.append(i)

        if len(second) > 0:
            if type(second[0]) == type(0):
                intervals.append(second)
            else:
                for i in second:
                    intervals.append(i)

    elif n == 1:
        intervals.append([a, b])

    return intervals

def RootsSearch(polinom__):
    polinom = [polinom__[i] for i in range(len(polinom__))]

    #   За вернюю границу возьмем границу, полученную методом Ньютона
    #   За нижнюю границу возьмем отриц внешний радиус круга на комплексн плоскоти,
    #       в котором лежат все корни полинома
    #   Затем с будем проверять интервал длинной в ед на наличее корней методом Штурма
    #   Если корней 2 и более будем делить интервал пополам и повторять прошлый шаг
    #   Далее на каждом интервале, который имеет корень методом дихотомии найдем этот корень

    upper_bound = Newton(polinom)
    intervals = []

    low, hiegh = LowUpBounds(polinom)

    hiegh = math.ceil(hiegh)

    for i in range(upper_bound, -hiegh - 1, -1):
        n = ShturmG(polinom, i - 1, i)
        if n > 1:
            for j in HelpFunction(polinom, i - 1, i):
                intervals.append(j)

        elif n == 1:
            intervals.append([i - 1, i])

    roots = []
    for i in intervals:
        roots.append(round(Dichotomy(polinom, i[0], i[1]), 4))

    return roots, intervals


def calculate():
    coefs = [float(a) for a in table_coefs.get().split()]

    lable_polinom['text'] = print_polinom(coefs)

    n = len(coefs) - 1
    for coef in coefs:
        if coef == 0:
            n -= 1
        else:
            break

    lable_power['text'] = str(n)

    roots, intervals = RootsSearch(coefs)

    lable_roots['text'] = ''
    for root in roots:
        lable_roots['text'] += str(root) + ' '

    lable_bounds['text'] = ''
    for interval in intervals:
        lable_bounds['text'] += str(round(interval[0], 4)) + ' ' + str(round(interval[1], 4)) + '\n'



def clean():
    table_coefs.delete(0, tk.END)
    lable_polinom['text'] = ''
    lable_power['text'] = ''
    lable_roots['text'] = ''
    lable_bounds['text'] = ''


window = tk.Tk()
window.title('Поиск корней методом дихотомии')

font_arial = tkFont.Font(family="Arial", size=14)

tk.Label(text="Коэфиценты:", font=font_arial).grid(row=0, column=0, sticky='w', pady=10, padx=10)
table_coefs = tk.Entry(font=font_arial)
table_coefs.grid(row=0, column=1, columnspan=3, sticky='we', padx=10)

tk.Label(text="Полином:", font=font_arial).grid(row=1, column=0, sticky='w', padx=10, pady=10)
lable_polinom = tk.Label(font=font_arial)
lable_polinom.grid(row=1, column=1, columnspan=2, sticky='w', padx=10)

tk.Label(text='Степень полинома:', font=font_arial).grid(row=2, column=0, sticky='w', padx=10, pady=10)
lable_power = tk.Label(font=font_arial)
lable_power.grid(row=2, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text='Корни полинома:', font=font_arial).grid(row=3, column=0, sticky='w', padx=10, pady=10)
lable_roots = tk.Label(font=font_arial)
lable_roots.grid(row=3, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text='Границы корней:', font=font_arial).grid(row=4, column=0, sticky='w', padx=10, pady=10)
lable_bounds = tk.Label(font=font_arial)
lable_bounds.grid(row=4, column=1, sticky='w', padx=10)

tk.Button(text="Вычислить", font=font_arial, command=calculate).grid(row=5, column=0, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", font=font_arial, command=clean).grid(row=5, column=3, padx=10, sticky='e')


tk.mainloop()