import tkinter as tk

def power(n_):
    if n_ == 2:
        return '\U000000B2'
    elif n_ == 3:
        return '\U000000B3'
    elif n_ == 4:
        return '\U00002074'
    elif n_ == 5:
        return '\U00002075'
    elif n_ == 6:
        return '\U00002076'
    elif n_ == 7:
        return '\U00002077'
    elif n_ == 8:
        return '\U00002078'
    elif n_ == 9:
        return '\U00002079'

def print_polinom(coefs_, x='x'):
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

def chord(coefs_):
    extremums = []
    if len(coefs_) > 2:  # запускаем рекурсию
        extremums = chord(differential(coefs_))

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

        if f(lower_bound, coefs_) == 0:
            roots.append(lower_bound)
        elif f(upper_bound, coefs_) == 0:
            roots.append(upper_bound)
        else:
            if f(lower_bound, coefs_) * f(upper_bound, coefs_) > 0:
                continue

            x, x_prev, i = lower_bound, upper_bound, 0
            while abs(x - x_prev) >= 0.0001 and i < 1000:
                x, x_prev, i = x - f(x, coefs_) / (f(x, coefs_) - f(x_prev, coefs_)) * (x - x_prev), x, i + 1

            roots.append(round(x, 4))
    return roots

def calculate():
    coefs = [float(a) for a in table_coefs.get().split()]

    lable_polinom['text'] = print_polinom(coefs)

    n = len(coefs) - 1
    for coef in coefs:
        if coef == 0:
            n -= 1
        else:
            break

    while coefs[0] == 0 and len(coefs) > 1:
        coefs.pop(0)

    lable_power['text'] = str(n)
    lable_roots['text'] = ''
    for root in chord(coefs):
        lable_roots['text'] += str(root) + ' '

    maxroot = -9999999999
    for root in chord(coefs):
        if root > maxroot:
            maxroot = root

    if maxroot == -9999999999:
        lable_maxroot['text'] = ''
    else:
        lable_maxroot['text'] = str(maxroot)

    if lable_roots['text'] == '':
        lable_roots['text'] = 'Действительных корней нет'

    upper_bound = find_bound(coefs)

    n = len(coefs) - 1
    if n % 2 == 0:  # delta = (-1)**n
        delta = 1
    else:
        delta = -1
    for i in range(n + 1):
        if (n - i) % 2 == 0:  # power = (-1)**(n - i)
            power = 1
        else:
            power = -1
        coefs[i] *= power * delta

    lower_bound = -find_bound(coefs)
    lable_lowbound['text'] = str(lower_bound)
    lable_upbound['text'] = str(upper_bound)

def clean():
    table_coefs.delete(0, tk.END)
    lable_polinom['text'] = ''
    lable_power['text'] = ''
    lable_roots['text'] = ''
    lable_maxroot['text'] = ''
    lable_lowbound['text'] = ''
    lable_upbound['text'] = ''


window = tk.Tk()
window.title('Поиск корней методом хорд')

tk.Label(text="Коэфиценты:").grid(row=0, column=0, sticky='w', pady=10, padx=10)
table_coefs = tk.Entry()
table_coefs.grid(row=0, column=1, columnspan=3, sticky='we', padx=10)

tk.Label(text="Полином:").grid(row=1, column=0, sticky='w', padx=10, pady=10)
lable_polinom = tk.Label()
lable_polinom.grid(row=1, column=1, columnspan=2, sticky='w', padx=10)

tk.Label(text='Степень полинома:').grid(row=2, column=0, sticky='w', padx=10, pady=10)
lable_power = tk.Label()
lable_power.grid(row=2, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text='Корни полинома:').grid(row=3, column=0, sticky='w', padx=10, pady=10)
lable_roots = tk.Label()
lable_roots.grid(row=3, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text='Максимальный корень:').grid(row=4, column=0, sticky='w', padx=10, pady=10)
lable_maxroot = tk.Label()
lable_maxroot.grid(row=4, column=1, columnspan=3, sticky='w', padx=10)


tk.Label(text='Нижняя граница:').grid(row=5, column=0, sticky='w', padx=10, pady=10)
lable_lowbound = tk.Label()
lable_lowbound.grid(row=5, column=1, sticky='w', padx=10)
tk.Label(text='Верхняя граница:').grid(row=5, column=2, sticky='w', padx=10, pady=10)
lable_upbound = tk.Label()
lable_upbound.grid(row=5, column=3, sticky='w', padx=10)

tk.Button(text="Вычислить", command=calculate).grid(row=6, column=0, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", command=clean).grid(row=6, column=3, padx=10, sticky='e')


tk.mainloop()
