# Гордионок Е.А.
# М8О-209Б-19
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
                print('+', end='')
        else:
            flag = False
            print('-', end='')

        if abs(coef) != 1 or n_ == 0:
            print(abs(coef), end='')
        if n_ == 0:
            continue
        elif n_ == 1:
            print(x, end='')
        else:
            print(x, power(n_), sep='', end='')

    print()


print('Введите коэфиценты: ', end='')
coefs = [float(a) for a in input().split()]
print('Введите точку: ', end='')
x = float(input())

print('Введенный многочлен f(x) = ', end='')

print_polinom(coefs)

n = len(coefs) - 1
for coef in coefs:
    if coef == 0:
        n -= 1
    else:
        break

print('Степень полинома:', n)

ans = coefs[0]
for i in range(1, len(coefs)):
    ans = coefs[i] + x * ans
print('Результат вычисления по схеме Горнера: f(', x, ') = ', ans, sep='')
