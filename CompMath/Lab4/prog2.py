import tkinter as tk

def getMatrixMinor(m, i, j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def m_det(m):
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*m_det(getMatrixMinor(m,0,c))
    return determinant

def m_mult(__lhs, __rhs):
    n = len(__lhs)
    m = len(__rhs[0])
    r = len(__rhs)
    matrix = [[0 for y in range(m)] for x in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(r):
                matrix[i][j] += __lhs[i][k] * __rhs[k][j]

    return matrix

def m_cmult(__mat, __c):
    n = len(__mat)
    m = len(__mat[0])
    return [[__mat[j][i] * __c for i in range(m)] for j in range(n)]

def m_sum(__lhs, __rhs):
    n = len(__lhs)
    m = len(__rhs[0])
    matrix = [[0 for y in range(m)] for x in range(n)]
    for i in range(n):
        for j in range(m):
            matrix[i][j] = __lhs[i][j] + __rhs[i][j]

    return matrix

def inverse_matrix_2x2(__mat):
    inv = [[0 for i in range(2)] for j in range(2)]
    inv[0][0] = __mat[1][1]
    inv[1][1] = __mat[0][0]
    inv[0][1] = -__mat[0][1]
    inv[1][0] = -__mat[1][0]

    return m_cmult(inv, (1 / m_det(__mat)))

def matrix_combine(P, Q, R, S):
    M = [[0 for i in range(len(P) + len(R))] for j in range(len(P[0]) + len(Q[0]))]
    for i in range(len(M)):
        for j in range(len(M[0])):
            if i < len(P) and j < len(P[0]):
                M[i][j] = P[i][j]
            elif i < len(Q) and j < len(P[0]) + len(Q[0]):
                M[i][j] = Q[i][j - len(P[0])]
            elif i < len(P) + len(R) and j < len(P[0]):
                M[i][j] = R[i - len(P)][j]
            elif i < len(P) + len(R) and j < len(P[0]) + len(Q[0]):
                M[i][j] = S[i - len(P)][j - len(P[0])]

    return M

def inverse_matrix(__mat):
    m = len(__mat)
    inverse_m = [[0 for i in range(m)] for j in range(m)]
    if m == 2:
        det = m_det(__mat)
        inverse_m[0][0] = __mat[1][1] / det
        inverse_m[0][1] = -__mat[0][1] / det
        inverse_m[1][0] = -__mat[1][0] / det
        inverse_m[1][1] = __mat[0][0] / det
        return inverse_m
    elif m == 1:
        inverse_m[0][0] = 1 / __mat[0][0]
        return inverse_m

    a11 = [[0 for i in range(m-1)] for j in range(m-1)]
    for i in range(m-1):
        for j in range(m-1):
            a11[i][j] = __mat[i][j]

    a11 = inverse_matrix(a11)

    a12 = [[0] for i in range(m - 1)]
    for i in range(m-1):
        a12[i][0] = __mat[i][m - 1]

    a21 = [[0 for i in range(m - 1)]]
    for i in range(m-1):
        a21[0][i] = __mat[m-1][i]

    a22 = [[0]]
    a22[0][0] = __mat[m-1][m-1]

    X = m_mult(a11, a12)
    Y = m_mult(a21, a11)
    T = m_sum(a22, m_cmult(m_mult(a21, X), -1))
    T[0][0] = 1 / T[0][0]

    a11 = m_sum(a11, m_mult(m_mult(X, T), Y))
    a12 = m_cmult(m_mult(X, T), -1)
    a21 = m_cmult(m_mult(T, Y), -1)
    a22 = T

    return matrix_combine(a11, a12, a21, a22)

def calculate():
    matrix_coefs = [list(map(float, i.split())) for i in table_matrix.get('1.0', tk.END).split('\n')]
    while (len(matrix_coefs[len(matrix_coefs) - 1])) == 0:
        matrix_coefs.pop()

    table_inv.delete('1.0', tk.END)
    if m_det(matrix_coefs) == 0:
        table_inv.insert(1.0, 'Не существует')
    else:
        inv_m = inverse_matrix(matrix_coefs)
        s = ''
        for i in inv_m:
            for j in i:
                if abs(j) == 0:
                    s += str(0) + ' '
                else:
                    s += str(round(j, 5)) + ' '
            s += '\n'
        table_inv.insert(1.0, s)

def clean():
    table_matrix.delete('1.0', tk.END)
    table_inv.delete('1.0', tk.END)

def check():
    matrix_coefs = [list(map(float, i.split())) for i in table_matrix.get('1.0', tk.END).split('\n')]
    while (len(matrix_coefs[len(matrix_coefs) - 1])) == 0:
        matrix_coefs.pop()

    table_inv.delete('1.0', tk.END)
    if m_det(matrix_coefs) == 0:
        table_inv.insert(1.0, 'Не существует')
    else:
        inv_m = inverse_matrix(inverse_matrix(matrix_coefs))
        s = ''
        for i in inv_m:
            for j in i:
                if abs(j) == 0:
                    s += str(0) + ' '
                else:
                    s += str(round(j, 5)) + ' '
            s += '\n'
        table_inv.insert(1.0, s)


window = tk.Tk()
window.title('Нахождение обратной матрицы через окаймляющие блоки')

tk.Label(text='Матрица').grid(row=0, column=0, sticky='w', pady=10, padx=10)
table_matrix = tk.Text(width=30, height=14)
table_matrix.grid(row=1, column=0, columnspan=2, sticky='we', padx=10)

tk.Label(text='Обратная матрица').grid(row=0, column=2, sticky='w', pady=10, padx=10)
table_inv = tk.Text(width=30, height=14)
table_inv.grid(row=1, column=2, columnspan=2, sticky='we', padx=10)


tk.Button(text="Вычислить", command=calculate).grid(row=2, column=0, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", command=clean).grid(row=2, column=3, padx=10, sticky='e')
tk.Button(text="Проверка", command=check).grid(row=2, column=1, padx=10, sticky='w')


tk.mainloop()
