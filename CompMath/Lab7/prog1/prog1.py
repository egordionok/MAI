from math import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
import tkinter.font as tkFont
import numpy as np
import matplotlib.pyplot as plt

# Метод Эйлера
def Euler(ddy, x, y0, h):
    y = [0 for i in range(len(x))]
    y[0] = y0
    for i in range(1, len(x)):
        y[i] = y[i - 1] + h * ddy(x[i - 1], y[i - 1])
    return y

# Модифицированный метод Эйлера
def EulerModificated(ddy, x, y0, h):
    y = [0 for i in range(len(x))]
    y[0] = y0
    for i in range(1, len(x)):
        forecast = y[i - 1] + h * ddy(x[i - 1], y[i - 1])  # прогноз
        y[i] = y[i - 1] + (h / 2) * (ddy(x[i - 1], y[i - 1]) + ddy(x[i], forecast))   # коррекция
    return y


# Метод Рунге-Кутта 4 порядка
def RungeKutta(ddy, x, y0, h):
    y = [0 for i in range(len(x))]
    y[0] = y0
    for i in range(1, len(x)):
        k1 = h * ddy(x[i - 1], y[i - 1])
        k2 = h * ddy(x[i - 1] + h / 2, y[i - 1] + k1 / 2)
        k3 = h * ddy(x[i - 1] + h / 2, y[i - 1] + k2 / 2)
        k4 = h * ddy(x[i - 1] + h / 2, y[i - 1] + k3)
        y[i] = y[i - 1] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return y


# Метод Адамса 3 порядка
def Adams(ddy, x, y0, h):
    y = [0 for i in range(len(x))]
    y[0] = y0
    y[1] = y[0] + h * ddy(x[0], y[0])
    y[2] = y[1] + h * ddy(x[1], y[1])

    for i in range(3, len(x)):
        k1 = ddy(x[i - 1], y[i - 1])
        k2 = ddy(x[i - 2], y[i - 2])
        k3 = ddy(x[i - 3], y[i - 3])
        y[i] = y[i - 1] + h * (23 * k1 - 16 * k2 + 5 * k3) / 12
    return y


def clear():
    entry_diff_function.delete(0, tk.END)
    entry_function.delete(0, tk.END)
    entry_interval.delete(0, tk.END)
    entry_step.delete(0, tk.END)
    entry_x0.delete(0, tk.END)
    entry_y0.delete(0, tk.END)



def readFile():
    clear()
    file = open(askopenfilename(), 'r')
    file_text = file.read().split('\n')
    entry_diff_function.insert(0, file_text[0])
    zeros = file_text[1].split()
    entry_x0.insert(0, zeros[1])
    entry_y0.insert(0, zeros[0])
    entry_interval.insert(0, file_text[2])
    entry_step.insert(0, file_text[3])
    if len(file_text) > 3:
        entry_function.insert(0, file_text[4])


def functionParce():
    function = lambda x, y: eval(entry_diff_function.get().strip(' '))
    interval = [float(a) for a in entry_interval.get().strip('[ ]').split(';')]
    step = float(entry_step.get())
    x0 = float(entry_x0.get())
    y0 = float(entry_y0.get())
    return function, interval, step, x0, y0


def count():
    function, interval, step, x0, y0 = functionParce()
    x_list = list(np.arange(interval[0], interval[1] + step / 2, step))
    euler = Euler(function, x_list, y0, step)
    euler_modif = EulerModificated(function, x_list, y0, step)
    runge_kutt = RungeKutta(function, x_list, y0, step)
    adams = Adams(function, x_list, y0, step)

    if entry_function.get().strip(' ') != '':
        y_lambda = lambda x: eval(entry_function.get().strip(' '))
        y = [y_lambda(x) for x in x_list]
        plt.plot(x_list, y, label="y(x)")
    if varE.get() == 1:
        plt.plot(x_list, euler, label="Euler")
    if varEM.get() == 1:
        plt.plot(x_list, euler_modif, label="EulerModificated")
    if varRK.get() == 1:
        plt.plot(x_list, runge_kutt, label="Runge-Kutta")
    if varA.get() == 1:
        plt.plot(x_list, adams, label="Adams")

    plt.legend(loc=2)
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

    return 0


window = tk.Tk()

window.title('Решение задачи Коши различными методами')
font_arial = tkFont.Font(family="Arial", size=14)

tk.Label(text="y' =", font=font_arial).grid(row=0, column=0, sticky='e', pady=10, padx=10)
entry_diff_function = tk.Entry(font=font_arial)
entry_diff_function.grid(row=0, column=1, columnspan=3, sticky='we', padx=10)

tk.Label(text="y =", font=font_arial).grid(row=1, column=0, sticky='e', pady=10, padx=10)
entry_function = tk.Entry(font=font_arial)
entry_function.grid(row=1, column=1, columnspan=3, sticky='we', padx=10)

tk.Label(text="y\U00002080 =", font=font_arial).grid(row=2, column=0, sticky='e', pady=10, padx=10)
entry_y0 = tk.entry_interval = tk.Entry(font=font_arial, width=10)
entry_y0.grid(row=2, column=1, sticky='w', padx=10)

tk.Label(text="x\U00002080 =", font=font_arial).grid(row=2, column=2, sticky='e', pady=10, padx=10)
entry_x0 = tk.entry_interval = tk.Entry(font=font_arial, width=10)
entry_x0.grid(row=2, column=3, sticky='w', padx=10)

tk.Label(text="Интервал:", font=font_arial).grid(row=3, column=0, sticky='w', pady=10, padx=10)
entry_interval = tk.Entry(font=font_arial, width=10)
entry_interval.grid(row=3, column=1, sticky='we', padx=10)

tk.Label(text="Шаг:", font=font_arial).grid(row=3, column=2, sticky='e', pady=10, padx=10)
entry_step = tk.Entry(font=font_arial, width=10)
entry_step.grid(row=3, column=3, sticky='we', padx=10)

varE = tk.IntVar()
varEM = tk.IntVar()
varRK = tk.IntVar()
varA = tk.IntVar()
varE.set(1)
varEM.set(1)
varRK.set(1)
varA.set(1)

check_box_euler = tk.Checkbutton(window, text='Euler', variable=varE, onvalue=1, offvalue=0)
check_box_euler.grid(row=4, column=0, pady=10, padx=10)
check_box_eulerM = tk.Checkbutton(window, text='EulerModificated', variable=varEM, onvalue=1, offvalue=0)
check_box_eulerM.grid(row=4, column=1, pady=10, padx=10)
check_box_rk = tk.Checkbutton(window, text='Runge-Kutta', variable=varRK, onvalue=1, offvalue=0)
check_box_rk.grid(row=4, column=2, pady=10, padx=10)
check_box_adams = tk.Checkbutton(window, text='Adams', variable=varA, onvalue=1, offvalue=0)
check_box_adams.grid(row=4, column=3, pady=10, padx=10)

tk.Button(text="Выбрать файл", command=readFile, font=font_arial). \
    grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky='w')
tk.Button(text="Расчет", command=count, font=font_arial). \
    grid(row=5, column=3, pady=10, padx=10, sticky='e')


window.mainloop()
