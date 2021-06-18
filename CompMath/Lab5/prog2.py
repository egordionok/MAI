import numpy as np
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

def find_bound(coefs_):
    xi = 1
    if coefs_[0] < 0:
        coefs_ = [-i for i in coefs_]

    while True:
        flag = True
        newcoefs = [coefs_[0]]
        for i in range(1, len(coefs_)):
            coef = coefs_[i] + newcoefs[i - 1] * xi
            if coef < 0:
                xi += 1
                flag = False
                break
            newcoefs.append(coef)
        if flag:
            break

    return xi

def f(x, coefs_):
    ans = coefs_[0]
    for i in range(1, len(coefs_)):
        ans = coefs_[i] + x * ans

    return ans

def differential(coefs_):
    n = len(coefs_) - 1
    newcoefs_ = []
    for i in range(len(coefs_) - 1):
        newcoefs_.append(coefs_[i] * n)
        n -= 1

    return newcoefs_

def dichotomy(coefs_):
    extremums = []
    if len(coefs_) > 2:  # запускаем рекурсию
        extremums = dichotomy(differential(coefs_))

    extremums.append(find_bound(coefs_))

    newcoefs = coefs_.copy()

    n = len(coefs_) - 1
    if n % 2 == 0:  # delta = (-1)**n
        delta = 1
    else:
        delta = -1
    for i in range(n + 1):
        if (n - i) % 2 == 0:  # power = (-1)**(n - i)
            power_ = 1
        else:
            power_ = -1
        newcoefs[i] *= power_ * delta

    extremums.insert(0, -find_bound(newcoefs))

    roots = []
    for i in range(len(extremums) - 1):
        upper_bound = extremums[i + 1]
        lower_bound = extremums[i]
        mid_x = (upper_bound + lower_bound) / 2

        if f(lower_bound, coefs_) == 0:
            roots.append(lower_bound)
        elif f(upper_bound, coefs_) == 0:
            roots.append(upper_bound)
        else:
            middle = f(mid_x, coefs_)
            if f(lower_bound, coefs_) * f(upper_bound, coefs_) > 0:
                continue
            while middle != 0:
                # print(mid_x)
                if middle * f(upper_bound, coefs_) < 0:
                    lower_bound = mid_x
                else:
                    upper_bound = mid_x

                mid_x = (upper_bound + lower_bound) / 2
                middle = round(f(mid_x, coefs_), 6)
            roots.append(mid_x)
    return roots

def Laverrye(__coefs):
    n = len(__coefs)

    arr = np.array(__coefs)
    dinarr = arr.copy()     # изменяющийся массив
    s = []

    for i in range(n):
        diag_sum = 0
        for j in range(n):  # след
            diag_sum += dinarr[j][j]

        s.append(diag_sum)
        dinarr = np.dot(dinarr, arr)

    p = []
    for i in range(n):
        pi = s[i]
        for j in range(i):
            pi += s[j]*p[i - j - 1]

        pi /= -(i + 1)
        p.append(pi)

    p.insert(0, 1)
    return p

def max_lambda(__coefs):
    n = len(__coefs)
    y = np.full((n, 1), 1, dtype=int)
    _A = np.array(__coefs)
    A = np.dot(_A, y)
    A_pre = np.copy(A)
    lamb = 0
    pre = 0
    for i in range(n):
        lamb += A[i][0]
    lamb /= n

    while abs(lamb - pre) / 2 > 0.001:
        pre = lamb
        lamb = 0
        A = np.dot(_A, A)
        for i in range(n):
            lamb += A[i][0] / A_pre[i][0]

        lamb /= n
        A_pre = A

    return lamb


def calculate():
    coefs = [list(map(float, i.split())) for i in table_coefs.get('1.0', tk.END).split('\n')]
    while (len(coefs[len(coefs) - 1])) == 0:
        coefs.pop()

    polinom = Laverrye(coefs)
    lable_polinom['text'] = ''
    lable_polinom['text'] = print_polinom(polinom)
    lable_roots['text'] = ''
    for root in dichotomy(polinom):
        lable_roots['text'] += str(round(root, 3)) + ' '
    lable_lambda['text'] = ''
    lable_lambda['text'] = str(round(max_lambda(coefs), 3))


def clean():
    table_coefs.delete(1.0, tk.END)
    lable_polinom['text'] = ''
    lable_lambda['text'] = ''
    lable_roots['text'] = ''


window = tk.Tk()
window.title('Нахождение характеристического полинома произвольной квадратной матрицы по методу Лаверрье')

font_arial = tkFont.Font(family="Arial", size=14)

tk.Label(text="Коэфиценты:", font=font_arial).grid(row=0, column=0, sticky='w', pady=10, padx=10)
table_coefs = tk.Text(width=21, height=10, font=font_arial)
table_coefs.grid(row=0, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text="Полином:", font=font_arial).grid(row=1, column=0, sticky='w', padx=10, pady=10)
lable_polinom = tk.Label(font=font_arial)
lable_polinom.grid(row=1, column=1, columnspan=2, sticky='w', padx=10)

tk.Label(text="Корни:", font=font_arial).grid(row=2, column=0, sticky='w', padx=10, pady=10)
lable_roots = tk.Label(font=font_arial)
lable_roots.grid(row=2, column=1, columnspan=2, sticky='w', padx=10)

tk.Label(text='λmax = ', font=font_arial).grid(row=3, column=0, sticky='w', padx=10, pady=10)
lable_lambda = tk.Label(font=font_arial)
lable_lambda.grid(row=3, column=1, columnspan=3, sticky='w', padx=10)


tk.Button(text="Вычислить", command=calculate, font=font_arial).grid(row=4, column=0, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", command=clean, font=font_arial).grid(row=4, column=3, padx=10, sticky='e')


tk.mainloop()
