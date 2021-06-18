import numpy as np
import tkinter as tk

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

def print_polinom(coefs_, x='λ'):
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

def Laverrye(__coefs):
    n = len(__coefs)

    arr = np.array(__coefs)
    dinarr = arr.copy()     # изменяющийся массив
    s = []  # суммы главных диагональных элементов

    for i in range(n):
        diag_sum = 0
        for j in range(n):
            diag_sum += dinarr[j][j]

        s.append(diag_sum)
        dinarr = np.dot(dinarr, arr)

    p = []  # коэфиценты характеремтического многочлена
    for i in range(n):
        pi = s[i]
        for j in range(i):
            pi += s[j]*p[i - j - 1]

        pi /= -(i + 1)
        p.append(pi)

    p.insert(0, 1)
    return p

def calculate():
    coefs = [list(map(float, i.split())) for i in table_coefs.get('1.0', tk.END).split('\n')]
    while (len(coefs[len(coefs) - 1])) == 0:
        coefs.pop()

    polinom = Laverrye(coefs)
    lable_polinom['text'] = ''
    lable_polinom['text'] = print_polinom(polinom)


def clean():
    table_coefs.delete(1.0, tk.END)
    lable_polinom['text'] = ''


window = tk.Tk()
window.title('Нахождение характеристического полинома произвольной квадратной матрицы по методу Лаверрье')

tk.Label(text="Коэфиценты:").grid(row=0, column=0, sticky='w', pady=10, padx=10)
table_coefs = tk.Text(width=21, height=10)
table_coefs.grid(row=0, column=1, columnspan=3, sticky='we', padx=10)

tk.Label(text="Полином:").grid(row=1, column=0, sticky='w', padx=10, pady=10)
lable_polinom = tk.Label()
lable_polinom.grid(row=1, column=1, columnspan=2, sticky='w', padx=10)


tk.Button(text="Вычислить", command=calculate).grid(row=4, column=0, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", command=clean).grid(row=4, column=3, padx=10, sticky='e')


tk.mainloop()