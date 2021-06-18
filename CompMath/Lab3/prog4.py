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


def Division(divd__, divr__):
    # Синтетическое деление

    divd = [divd__[i] for i in range(len(divd__))]
    divr = [divr__[i] for i in range(len(divr__))]
    divd_n = len(divd)
    divr_n = len(divr)
    result = [0 for i in range(divd_n)]

    for i in range(1, divr_n):  # берем коэффициенты делителя с обратным знаком
        divr[i] *= -1

    for i in range(divd_n - divr_n + 1):
        result[i] = divd[i] / divr[0]   # Поделим последний коэффициент в строке остатка на старший коэффициент делителя
        for j in range(1, divr_n):
            #   Умножим диагональ с коэффициентами делителя на крайний левый коэффициент из строки результатов
            #   Выполним сложение значений в следующем столбце
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


def calculate():
    coefs1 = [float(a) for a in table_coefs1.get().split()]
    coefs2 = [float(a) for a in table_coefs2.get().split()]

    lable_polinom1['text'] = print_polinom(coefs1)
    lable_polinom2['text'] = print_polinom(coefs2)

    chast, ost = Division(coefs1, coefs2)

    lable_chast['text'] = print_polinom(chast)
    lable_ost['text'] = print_polinom(ost)


def clean():
    table_coefs1.delete(0, tk.END)
    lable_polinom1['text'] = ''
    table_coefs2.delete(0, tk.END)
    lable_polinom2['text'] = ''
    lable_chast['text'] = ''
    lable_ost['text'] = ''


window = tk.Tk()
window.title('Деление полинома на полином')

font_arial = tkFont.Font(family="Arial", size=14)

tk.Label(text="Делимое :", font=font_arial).grid(row=0, column=0, sticky='w', pady=10, padx=10)
table_coefs1 = tk.Entry(font=font_arial)
table_coefs1.grid(row=0, column=1, columnspan=3, sticky='we', padx=10)

tk.Label(text="Полином:", font=font_arial).grid(row=1, column=0, sticky='w', padx=10, pady=10)
lable_polinom1 = tk.Label(font=font_arial)
lable_polinom1.grid(row=1, column=2, columnspan=2, sticky='w', padx=10)

tk.Label(text="Делитель:", font=font_arial).grid(row=2, column=0, sticky='w', pady=10, padx=10)
table_coefs2 = tk.Entry(font=font_arial)
table_coefs2.grid(row=2, column=1, columnspan=3, sticky='we', padx=10)

tk.Label(text="Полином:", font=font_arial).grid(row=3, column=0, sticky='w', padx=10, pady=10)
lable_polinom2 = tk.Label(font=font_arial)
lable_polinom2.grid(row=3, column=2, columnspan=2, sticky='w', padx=10)

tk.Label(text="Частное:", font=font_arial).grid(row=4, column=0, sticky='w', padx=10, pady=10)
lable_chast = tk.Label(font=font_arial)
lable_chast.grid(row=4, column=2, columnspan=2, sticky='w', padx=10)

tk.Label(text="Остаток:", font=font_arial).grid(row=5, column=0, sticky='w', padx=10, pady=10)
lable_ost = tk.Label(font=font_arial)
lable_ost.grid(row=5, column=2, columnspan=2, sticky='w', padx=10)



tk.Button(text="Вычислить", font=font_arial, command=calculate).grid(row=6, column=0, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", font=font_arial, command=clean).grid(row=6, column=3, padx=10, sticky='e')


tk.mainloop()