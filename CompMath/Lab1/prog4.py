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

def find_bound(coefs_):
    xi = 1
    if coefs_[0] < 0:
        coefs_ = [-i for i in coefs_]

    while True:
        flag = True
        newcoefs = [coefs_[0]]
        for i in range(1, len(coefs_)):
            coef = coefs_[i] + newcoefs[i - 1] * xi
            if coef < 0:
                xi += 1
                flag = False
                break
            newcoefs.append(coef)
        if flag:
            break

    return xi


print('Введите коэфиценты: ', end='')
coefs = [float(a) for a in input().split()]

print('Введенный многочлен f(x) = ', end='')
print_polinom(coefs)

n = len(coefs) - 1
for coef in coefs:
    if coef == 0:
        n -= 1
    else:
        break

print('Степень полинома:', n)

upper_bound = find_bound(coefs)

n = len(coefs) - 1
if n % 2 == 0:  # delta = (-1)**n
    delta = 1
else:
    delta = -1
for i in range(n + 1):
    if (n - i) % 2 == 0:  # power = (-1)**(n - i)
        power = 1
    else:
        power = -1
    coefs[i] *= power * delta

lower_bound = -find_bound(coefs)

print('Границы корней:', lower_bound, '<= x <=',  upper_bound)

# [1,0,-12,-16,0]
# [2,-13,1,103,-183,90]
# [-2,-13,-13,28]
# [0,0,5,-16,-45,0]
