import tkinter as tk
import tkinter.font as tkFont
from copy import copy


def StringSwap(arr, n, m):
    for i in range(len(arr[0])):
        arr[n][i], arr[m][i] = arr[m][i], arr[n][i]


def Gauss(arr):
    A = [[arr[i][j] for j in range(len(arr[i]))] for i in range(len(arr))]

    #   Прямой ход
    for k in range(len(A)):
        akk = A[k][k]
        for i in range(len(A[k])):
            A[k][i] = A[k][i] / akk

        for i in range(k + 1, len(A)):
            K = A[i][k] / A[k][k]
            for j in range(len(A[i])):
                A[i][j] = A[i][j] - A[k][j] * K

    #   Обратныйход (Зануление верхнего правого угла)
    for k in range(len(A)):
        for i in range(len(A) - 1, -1, -1):
            A[k][i] = A[k][i] / A[k][k]

        for i in range(k - 1, -1, -1):
            K = A[i][k] / A[k][k]
            for j in range(len(A[i]) - 1, -1, -1):
                A[i][j] = A[i][j] - A[k][j] * K

    answer = []
    for i in range(len(A)):
        answer.append(A[i].pop())

    return answer


def Calculate():
    arr = [list(map(float, i.split())) for i in table_coefs.get('1.0', tk.END).split('\n')]

    while (len(arr[len(arr) - 1])) == 0:
        arr.pop()

    ans = ''
    for i in Gauss(arr):
        ans += str(round(i, 4)) + ' '

    entry_roots.delete(0, tk.END)
    entry_roots.insert(0, ans)


def Clean():
    table_coefs.delete('1.0', tk.END)
    entry_roots.delete(0, tk.END)


window = tk.Tk()
window.title('Решение СЛАУ методом Гауса')

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
