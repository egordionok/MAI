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

def print_polinom(__coefs, __x='x', __y='y'):
    __n = len(__coefs)
    __polinom = ''
    flag = True

    for str_coefs in __coefs:
        __n -= 1
        __m = len(str_coefs)
        for coef in str_coefs:
            __m -= 1
            if coef == 0:
                continue
            if coef >= 0:
                if flag:
                    flag = False
                else:
                    __polinom += '+'
            else:
                flag = False
                __polinom += '-'

            if abs(coef) != 1 or (__m == 0 and __n == 0):
                __polinom += str(abs(coef))

            if __n == 1:
                __polinom += __y
            elif __n > 1:
                __polinom += __y + power(__n)
            if __m == 1:
                __polinom += __x
            elif __m > 1:
                __polinom += __x + power(__m)

    return __polinom

def gorner(x, __coefs):
    ans = __coefs[0]
    for i in range(1, len(__coefs)):
        ans = __coefs[i] + x * ans

    return ans

def gornerXY(x, y,  __coefs):
    __coefs_for_y = []
    for i in __coefs:
        __coefs_for_y.append(gorner(x, i))

    return gorner(y, __coefs_for_y)

def calculate():

    __coefs = [list(map(float, i.split())) for i in table_coefs.get('1.0', tk.END).split('\n')]
    while(len(__coefs[len(__coefs) - 1])) == 0:
        __coefs.pop()

    __x, __y = float(x_entry.get()), float(y_entry.get())

    lable_polinom['text'] = print_polinom(__coefs)
    value_polinom_lable['text'] = str(gornerXY(__x, __y, __coefs))


def clean():
    table_coefs.delete('1.0', tk.END)
    lable_polinom['text'] = ''
    value_polinom_lable['text'] = ''
    x_entry.delete(0, tk.END)
    y_entry.delete(0, tk.END)


window = tk.Tk()
window.title('Значение полинома от двух переменных')

tk.Label(text="Коэфиценты:").grid(row=0, column=0, sticky='w', pady=10, padx=10)
table_coefs = tk.Text(width=21, height=10)
table_coefs.grid(row=0, column=1, columnspan=3, sticky='we', padx=10)

tk.Label(text="x:").grid(row=1, column=0, sticky='e', pady=10, padx=10)
x_entry = tk.Entry()
x_entry.grid(row=1, column=1, sticky='we', padx=10)

tk.Label(text="y:").grid(row=1, column=2, sticky='e', pady=10, padx=10)
y_entry = tk.Entry()
y_entry.grid(row=1, column=3, sticky='we', padx=10)

tk.Label(text="Полином:").grid(row=2, column=0, sticky='w', padx=10, pady=10)
lable_polinom = tk.Label()
lable_polinom.grid(row=2, column=1, columnspan=2, sticky='w', padx=10)

tk.Label(text='Значение полинома в точке (x, y):').grid(row=3, column=0, columnspan=2, sticky='w', padx=10, pady=10)
value_polinom_lable = tk.Label()
value_polinom_lable.grid(row=3, column=2, columnspan=2, sticky='w', padx=10)

tk.Button(text="Вычислить", command=calculate).grid(row=4, column=0, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", command=clean).grid(row=4, column=3, padx=10, sticky='e')


tk.mainloop()
