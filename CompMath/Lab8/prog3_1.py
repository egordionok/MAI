import tkinter as tk
import tkinter.font as tkFont
import numpy as np
import math


def vector_norm(x):
    m = math.fabs(x[0])
    for i in x:
        if math.fabs(i) > m:
            m = math.fabs(i)
    return m


def SimpleIterations(arr):
    A = [[arr[i][j] for j in range(len(arr[i]) - 1)] for i in range(len(arr))]
    n = len(A)
    B = [arr[i][len(A[0])] for i in range(n)]

    alpha = np.array([[-A[i][j] / A[i][i] for j in range(n)] for i in range(n)])
    for i in range(n):
        alpha[i][i] = 0
    betta = np.array([B[i] / A[i][i] for i in range(n)])

    x = np.copy(betta)
    eps = 1

    while eps >= 0.0001:
        x_last = x
        x = np.dot(alpha, x) + betta
        eps = vector_norm(x - x_last)

    return x


def Calculate():
    arr = [list(map(float, i.split())) for i in table_coefs.get('1.0', tk.END).split('\n')]

    while (len(arr[len(arr) - 1])) == 0:
        arr.pop()

    ans = ''
    for i in SimpleIterations(arr):
        ans += str(round(i, 4)) + ' '

    entry_roots.delete(0, tk.END)
    entry_roots.insert(0, ans)


def Clean():
    table_coefs.delete('1.0', tk.END)
    entry_roots.delete(0, tk.END)


window = tk.Tk()
window.title('Решение СЛАУ методом простых итераций')

font_arial = tkFont.Font(family="Arial", size=14)

tk.Label(text="A|B =", font=font_arial).grid(row=0, column=0, sticky='e', pady=10, padx=10)
table_coefs = tk.Text(width=21, height=10, font=font_arial)
table_coefs.grid(row=0, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text="x\U00002081, x\U00002082, ... :", font=font_arial).grid(row=2, column=0, sticky='e', padx=10, pady=10)
entry_roots = tk.Entry(font=font_arial)
entry_roots.grid(row=2, column=1, columnspan=3, sticky='w', padx=10)

tk.Button(text="Вычислить", command=Calculate, font=font_arial).grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", command=Clean, font=font_arial).grid(row=4, column=3, padx=10, sticky='e')


tk.mainloop()
