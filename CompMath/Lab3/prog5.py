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
        if abs(coefs[i]) > A and i != 0:
            A = abs(coefs[i])
        if abs(coefs[i]) > B and i != len(coefs) - 1:
            B = abs(coefs[i])

    return 1 / (1 + B / abs(coefs[len(coefs) - 1])), 1 + A / abs(coefs[0])

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

def Shturm(polinom__):
    polinom = [polinom__[i] for i in range(len(polinom__))]

    if polinom[0] < 0:
        for i in range(len(polinom)):
            polinom[i] *= -1

    shturm_system = []
    shturm_system.append(polinom)
    shturm_system.append(Derivative(polinom))
    n = 1
    while True:     # Формируем систему Штурма
        res, ost = Division(shturm_system[n - 1], shturm_system[n])
        for i in range(len(ost)):
            ost[i] *= -1

        if len(ost) == 0:
            break
        shturm_system.append(ost)
        n += 1

    Nl = 0
    Nu = 0
    inf = float("inf")

    for i in range(0, len(shturm_system) - 1):  # Вычисляем число-во перемен знаков для границ
        if Gorner(shturm_system[i], -inf) * Gorner(shturm_system[i + 1], -inf) < 0:
            Nl += 1
        if Gorner(shturm_system[i], inf) * Gorner(shturm_system[i + 1], inf) < 0:
            Nu += 1

    return Nl - Nu

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
    lable_roots['text'] = str(Shturm(coefs))



def clean():
    table_coefs.delete(0, tk.END)
    lable_polinom['text'] = ''
    lable_power['text'] = ''
    lable_roots['text'] = ''



window = tk.Tk()
window.title('Количество действительных корней по методу Штурма')

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

tk.Label(text='Кол-во корней:', font=font_arial).grid(row=3, column=0, sticky='w', padx=10, pady=10)
lable_roots = tk.Label(font=font_arial)
lable_roots.grid(row=3, column=1, columnspan=3, sticky='w', padx=10)


tk.Button(text="Вычислить", font=font_arial, command=calculate).grid(row=5, column=0, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", font=font_arial, command=clean).grid(row=5, column=3, padx=10, sticky='e')


tk.mainloop()
