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

    if len(newcoefs_) == 0:
        newcoefs_.append(0)

    return newcoefs_

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
    lable_diff['text'] = ''
    if len(differential(coefs)) == 1 and differential(coefs)[0] == 0:
        lable_diff['text'] = '0'
    else:
        lable_diff['text'] = print_polinom(differential(coefs))

def clean():
    table_coefs.delete(0, tk.END)
    lable_polinom['text'] = ''
    lable_power['text'] = ''
    lable_diff['text'] = ''



window = tk.Tk()
window.title('Поиск производной')

tk.Label(text="Коэфиценты:").grid(row=0, column=0, sticky='w', pady=10, padx=10)
table_coefs = tk.Entry()
table_coefs.grid(row=0, column=1, columnspan=3, sticky='we', padx=10)

tk.Label(text="Полином:").grid(row=1, column=0, sticky='w', padx=10, pady=10)
lable_polinom = tk.Label()
lable_polinom.grid(row=1, column=1, columnspan=2, sticky='w', padx=10)

tk.Label(text='Степень полинома:').grid(row=2, column=0, sticky='w', padx=10, pady=10)
lable_power = tk.Label()
lable_power.grid(row=2, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text='Производная полинома:').grid(row=3, column=0, sticky='w', padx=10, pady=10)
lable_diff = tk.Label()
lable_diff.grid(row=3, column=1, columnspan=3, sticky='w', padx=10)

tk.Button(text="Вычислить", command=calculate).grid(row=4, column=0, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", command=clean).grid(row=4, column=3, padx=10, sticky='e')


tk.mainloop()