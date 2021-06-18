import tkinter as tk
import tkinter.font as tkFont

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

def derivative(coefs__):
    coefs_ = [coefs__[i] for i in range(len(coefs__))]
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

def Lagrange(coefs__):
    coefs = [coefs__[i] for i in range(len(coefs__))]
    while coefs[len(coefs) - 1] == 0:
        coefs.pop()

    while coefs[0] == 0:
        coefs = coefs[1:]

    if coefs[0] < 0:
        for i in range(len(coefs)):
            coefs[i] = - coefs[i]

    B = 0
    k = 0

    for i in range(len(coefs)):
        if -coefs[i] > B and coefs[i] < 0:  # наибольшаи из абсол величин отриц коэф
            B = -coefs[i]
        if k == 0 and coefs[i] < 0 and i > 0:   # первый из отриц коэф полинома
            k = i

    if B == 0:
        return 0

    return 1 + (B / coefs[0]) ** (1 / k)

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
        coefs = derivative(coefs)

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
    l, u = LowUpBounds(coefs)

    lable_lowbound['text'] = str(round(l, 4))
    lable_upbound['text'] = str(round(u, 4))
    lable_lagrange['text'] = str(round(Lagrange(coefs), 4))
    lable_newton['text'] = str(round(Newton(coefs), 4))


def clean():
    table_coefs.delete(0, tk.END)
    lable_polinom['text'] = ''
    lable_power['text'] = ''
    lable_lowbound['text'] = ''
    lable_upbound['text'] = ''
    lable_lagrange['text'] = ''
    lable_newton['text'] = ''


window = tk.Tk()
window.title('Определение границ полинома')

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

tk.Label(text='Нижняя граница:', font=font_arial).grid(row=3, column=0, sticky='w', padx=10, pady=10)
lable_lowbound = tk.Label(font=font_arial)
lable_lowbound.grid(row=3, column=1, sticky='w', padx=10)
tk.Label(text='Верхняя граница:', font=font_arial).grid(row=3, column=2, sticky='w', padx=10, pady=10)
lable_upbound = tk.Label(font=font_arial)
lable_upbound.grid(row=3, column=3, sticky='w', padx=10)

tk.Label(text='Верхняя граница методом Лагранжа:', font=font_arial).grid(row=4, column=0, columnspan=2, sticky='w', padx=10, pady=10)
lable_lagrange = tk.Label(font=font_arial)
lable_lagrange.grid(row=4, column=2, sticky='w', padx=10)

tk.Label(text='Верхняя граница методом Ньютона:', font=font_arial).grid(row=5, column=0, columnspan=2, sticky='w', padx=10, pady=10)
lable_newton = tk.Label(font=font_arial)
lable_newton.grid(row=5, column=2, sticky='w', padx=10)

tk.Button(text="Вычислить", font=font_arial, command=calculate).grid(row=7, column=0, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", font=font_arial, command=clean).grid(row=7, column=3, padx=10, sticky='e')


tk.mainloop()
