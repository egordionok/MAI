import tkinter as tk

def column_line_out(__mat, m, p, q):
    H = [[0 for i in range(m - 1)] for j in range(m - 1)]
    for i in range(m - 1):
        for j in range(m - 1):
            if i >= p and j >= q:
                H[i][j] = __mat[i+1][j+1]
            elif i >= p and j < q:
                H[i][j] = __mat[i+1][j]
            elif j >= q and i < p:
                H[i][j] = __mat[i][j+1]
            elif i < p and j < q:
                H[i][j] = __mat[i][j]

    return H

def Det(__mat, m):
    flag = False
    p = -1
    q = -1
    k = 1
    while m != 2:
        # поиск p  и  q и элемента равного 1
        while not flag:
            for i in range(m):
                for j in range(m):
                    if __mat[i][j] == 1:
                        p = i
                        q = j
                        flag = True
                        break
                if flag:
                    break

            if not flag:
                p = 0
                q = 0
                k = __mat[0][0]
                for i in range(m):
                    __mat[i][0] = __mat[i][0] / k

                flag = True

        M = [[0 for i in range(m)] for j in range(m)]
        for i in range(m):
            for j in range(m):
                M[i][j] = __mat[i][j] - __mat[i][q] * __mat[p][j]

        __mat = column_line_out(M, m, p, q)
        m -= 1
        flag = False

    return k * (__mat[0][0] * __mat[1][1] - __mat[0][1] * __mat[1][0])

def calculate():
    matrix_coefs = [list(map(float, i.split())) for i in table_matrix.get('1.0', tk.END).split('\n')]
    while (len(matrix_coefs[len(matrix_coefs) - 1])) == 0:
        matrix_coefs.pop()

    Entry.delete(0, tk.END)
    Entry.insert(1, str(round(Det(matrix_coefs, len(matrix_coefs)), 3)))

def clean():
    table_matrix.delete('1.0', tk.END)
    Entry.delete(0, tk.END)


window = tk.Tk()
window.title('Нахождение определителя матрицы через элементарные преобразования')

tk.Label(text='Матрица').grid(row=0, column=0, columnspan=2, sticky='w', pady=10, padx=10)
table_matrix = tk.Text(width=21, height=10)
table_matrix.grid(row=1, column=0, columnspan=2, sticky='we', padx=10)

tk.Label(text='Определитель').grid(row=2, column=0, columnspan=2, sticky='w', pady=10, padx=10)
Entry = tk.Entry()
Entry.grid(row=2, column=1, columnspan=1, sticky='we', padx=10)


tk.Button(text="Вычислить", command=calculate).grid(row=3, column=0, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", command=clean).grid(row=3, column=1, padx=10, sticky='e')


tk.mainloop()
