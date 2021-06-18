import tkinter as tk
import tkinter.font as tkFont

def split_matrix(__maxtrix):
    n = len(__maxtrix)
    ans = []
    for i in range(0, n, 2):
        ans.append([])
        for j in range(0, n, 2):
            a = [[]]
            a[0].append(__maxtrix[i][j])
            if j + 1 < n:
                a[0].append(__maxtrix[i][j+1])
            if i+1 < n:
                a.append([])
                a[1].append(__maxtrix[i+1][j])
            if j+1 < n and i+1 < n:
                a[1].append(__maxtrix[i+1][j + 1])

            ans[i//2].append(a)

    return ans

def m_multiplication(__lhs, __rhs):
    n = len(__lhs)
    m = len(__rhs[0])
    r = len(__rhs)
    matrix = [[0 for y in range(m)] for x in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(r):
                matrix[i][j] += __lhs[i][k] * __rhs[k][j]

    return matrix

def m_sum(__lhs, __rhs):
    n = len(__lhs)
    m = len(__rhs[0])
    matrix = [[0 for y in range(m)] for x in range(n)]
    for i in range(n):
        for j in range(m):
            matrix[i][j] = __lhs[i][j] + __rhs[i][j]

    return matrix

def block_mult(__lhs, __rhs):
    n = len(__lhs)
    m = len(__rhs[0])
    r = len(__rhs)
    matrix = [[0 for y in range(m)] for x in range(n)]
    for i in range(n):
        for j in range(m):
            matrix[i][j] = [[0 for y in range(len(__lhs[0][j][0]))] for x in range(len(__lhs[i][0]))]
            for k in range(r):
                matrix[i][j] = m_sum(matrix[i][j], m_multiplication(__lhs[i][k], __rhs[k][j]))

    return matrix

def block_to_list(__matrix):
    arr = []
    n = -1  
    for i in __matrix:              # строка блоков
        arr.append([])
        n += 1
        for j in i:                 # блок в строке
            for k in j[0]:          # строка1 в блоке
                arr[n].append(k)
        arr.append([])
        n += 1
        for j in i:                 # блок в строке
            if len(j) > 1:
                for k in j[1]:      # строка2 в блоке
                    arr[n].append(k)

    return arr

def calculate():
    __lhs_coefs = [list(map(float, i.split())) for i in table_lhs.get('1.0', tk.END).split('\n')]
    __rhs_coefs = [list(map(float, i.split())) for i in table_rhs.get('1.0', tk.END).split('\n')]
    while(len(__lhs_coefs[len(__lhs_coefs) - 1])) == 0:
        __lhs_coefs.pop()

    while (len(__rhs_coefs[len(__rhs_coefs) - 1])) == 0:
        __rhs_coefs.pop()

    l = split_matrix(__lhs_coefs)
    r = split_matrix(__rhs_coefs)

    ans = block_to_list(block_mult(l, r))

    s = ''
    for i in ans:
        for j in i:
            s += str(j) + ' '

        s += '\n'

    table_answer.delete('1.0', tk.END)
    table_answer.insert(1.0, s)


def clean():
    table_lhs.delete('1.0', tk.END)
    table_rhs.delete('1.0', tk.END)
    table_answer.delete('1.0', tk.END)


window = tk.Tk()
window.title('Умножение квадратных матриц разложением на блоки')

fontStyle = tkFont.Font(family="Lucida Grande", size=22)

table_lhs = tk.Text(width=21, height=10)
table_lhs.grid(row=0, column=0, sticky='we', padx=10)

tk.Label(text='*', font=fontStyle).grid(row=0, column=1, sticky='w', pady=10, padx=10)
table_rhs = tk.Text(width=21, height=10)
table_rhs.grid(row=0, column=2, sticky='we', padx=10)

tk.Label(text='=', font=fontStyle).grid(row=0, column=3, sticky='w', pady=10, padx=10)
table_answer = tk.Text(width=21, height=10)
table_answer.grid(row=0, column=4, sticky='we', padx=10)

tk.Button(text="Вычислить", command=calculate).grid(row=1, column=0, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", command=clean).grid(row=1, column=4, padx=10, sticky='e')


tk.mainloop()