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
print('Введите число a: ', end='')
a = float(input())

print('Введенный многочлен f(x) = ', end='')
print_polinom(coefs)

n = len(coefs) - 1
for coef in coefs:
    if coef == 0:
        n -= 1
    else:
        break

print('Степень полинома:', n)

ans = 0
for i in range(1, len(coefs)):
    ans = coefs[i] + a * ans

newcoefs = []
n = len(coefs)
for i in range(n):
    deltcoefs = [coefs[0]]
    for j in range(1, len(coefs)):
        deltcoefs.append(coefs[j] + deltcoefs[j-1] * a)

    newcoefs.append(deltcoefs.pop())
    coefs = deltcoefs

newcoefs.reverse()

# if a >= 0:
#     a_str = '- ' + str(a)
# else:
#     a_str = '+ ' + str(-a)
print('Получен многочлен g(y) = ', sep='', end='')
print_polinom(newcoefs, 'y')
print('Коэфиценты многочлена:', newcoefs)

# [1,-8,5,2,-7] 2
# [1,-3,-12,52,-48] 3
# [1,13,57,83,-34,-120,0] -1