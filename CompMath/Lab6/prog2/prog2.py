import tkinter as tk
from tkinter.filedialog import askopenfilename
import tkinter.font as tkFont

import numpy as np
import matplotlib.pyplot as plt
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


class Function:
    y_list, x_list, y_der_list, delta_y = [], [], [], [[]]
    x_begin, x_end, x_delta = 0, 0, 0
    func = None

    def __init__(self, func, x_begin, x_end, x_delta):
        self.func = func
        self.x_list = list(np.arange(x_begin, x_end + x_delta / 2, x_delta))
        self.y_list = [func(x) for x in self.x_list]
        self.x_begin = x_begin
        self.x_end = x_end
        self.x_delta = x_delta

    def integral(self):
        y = self.y_list.copy()
        y_0 = y.pop(0)
        y_n = y.pop()

        sigma_1 = 0
        sigma_2 = 0

        for i in range(len(y)):
            if i % 2 == 0:
                sigma_1 += y[i]
            else:
                sigma_2 += y[i]

        return self.x_delta / 3 * (y_0 + y_n + 4 * sigma_1 + 2 * sigma_2)

    def derCount(self):
        self.delta_y = [[] for i in range(len(self.y_list))]
        self.y_der_list = []

        for i in range(len(self.y_list)):
            self.delta_y[i].append(self.y_list[i])

        for i in range(8):
            delta_i = []

            for k in range(len(self.y_list) - i - 1):
                delta_i.append(self.delta_y[k + 1][i] - self.delta_y[k][i])

            for k in range(len(delta_i)):
                self.delta_y[k].append(delta_i[k])

        for i in range(len(self.delta_y)):
            y_der = 0
            for k in range(1, len(self.delta_y[i])):
                y_der += (self.delta_y[i][k] / k) * ((-1) ** k)

            self.y_der_list.append(y_der / self.x_delta)

    def showFunction(self):
        plt.plot(self.x_list, self.y_list)
        plt.legend(["y(x)"], loc=1)
        plt.grid(True)
        plt.show()

    def showFunctionWithDer(self):
        self.derCount()
        plt.plot(self.x_list, self.y_list, self.x_list, self.y_der_list)
        plt.grid(True)
        plt.legend(["y(x)", "y'(x)"], loc=1)
        self.printTable()
        plt.show()

    def printTable(self):
        for i in range(len(self.delta_y[0])):
            if i == 0:
                print('y',  end='\t\t')
            else:
                print('??' + power(i) + 'y', end='\t\t')

        print()

        for delta in self.delta_y:
            for y in delta:
                if len(str(round(y, 4))) < 4:
                    print(round(y, 4), end='\t\t')
                else:
                    print(round(y, 4), end='\t')

            print()


class MainWindow(tk.Tk):
    entry_function, entry_interval, entry_step, entry_answer = None, None, None, None
    function = None

    def __init__(self):
        super().__init__()
        self.title('???????????????????? ???????????????????????? ???????????????? ?????????????????????? ???? ???????????????? ???????????????? ??????????????')
        font_arial = tkFont.Font(family="Arial", size=14)

        tk.Label(text="f(x) =", font=font_arial).grid(row=0, column=0, sticky='e', pady=10, padx=10)
        self.entry_function = tk.Entry(font=font_arial)
        self.entry_function.grid(row=0, column=1, columnspan=3, sticky='we', padx=10)

        tk.Label(text="????????????????:", font=font_arial).grid(row=1, column=0, sticky='e', pady=10, padx=10)
        self.entry_interval = tk.Entry(font=font_arial, width=10)
        self.entry_interval.grid(row=1, column=1, sticky='we', padx=10)

        tk.Label(text="??????:", font=font_arial).grid(row=1, column=2, sticky='e', pady=10, padx=10)
        self.entry_step = tk.Entry(font=font_arial, width=10)
        self.entry_step.grid(row=1, column=3, sticky='w', padx=10)

        tk.Label(text="???????????????? ??????????????????:", font=font_arial).\
            grid(row=2, column=0, sticky='w', pady=10, padx=10)
        self.entry_answer = tk.Entry(font=font_arial, width=10)
        self.entry_answer.grid(row=2, column=1, sticky='w', padx=10)

        tk.Button(text="?????????????? ????????", command=self.readFile, font=font_arial).\
            grid(row=3, column=0, pady=10, padx=10, sticky='w')
        tk.Button(text="????????????", command=self.graph, font=font_arial).\
            grid(row=3, column=2, pady=10, padx=10, sticky='e')
        tk.Button(text="????????????", command=self.count, font=font_arial).\
            grid(row=3, column=3, pady=10, padx=10, sticky='e')

    def clear(self):
        self.entry_function.delete(0, tk.END)
        self.entry_interval.delete(0, tk.END)
        self.entry_step.delete(0, tk.END)
        self.entry_answer.delete(0, tk.END)

    def readFile(self):
        self.clear()
        file = open(askopenfilename(), 'r')
        file_text = file.read().split('\n')
        self.entry_function.insert(0, file_text[0])
        self.entry_interval.insert(0, file_text[1])
        self.entry_step.insert(0, file_text[2])

    def functionParce(self):
        function = lambda x: eval(self.entry_function.get().strip(' '))
        interval = [float(a) for a in self.entry_interval.get().strip('[ ]').split(';')]
        step = float(self.entry_step.get())

        return function, interval, step

    def graph(self):
        function_table, interval, step = self.functionParce()
        self.function = Function(function_table, interval[0], interval[1], step)
        self.function.showFunction()
        # self.function.showFunctionWithDer()

    def count(self):
        function_table, interval, step = self.functionParce()
        self.function = Function(function_table, interval[0], interval[1], step)
        self.entry_answer.delete(0, tk.END)
        self.entry_answer.insert(0, str(round(self.function.integral(), 4)))


if __name__ == "__main__":
    window = MainWindow()
    window.mainloop()
