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

def f(x, coefs_):
    ans = coefs_[0]
    for i in range(1, len(coefs_)):
        ans = coefs_[i] + x * ans

    return ans

def differential(coefs_):
    n = len(coefs_) - 1
    newcoefs_ = []
    for i in range(len(coefs_) - 1):
        newcoefs_.append(coefs_[i] * n)
        n -= 1

    return newcoefs_

def dichotomy(coefs_):
    extremums = []
    if len(coefs_) > 2:  # запускаем рекурсию
        extremums = dichotomy(differential(coefs_))

    extremums.append(find_bound(coefs_))

    newcoefs = coefs_.copy()

    n = len(coefs_) - 1
    if n % 2 == 0:  # delta = (-1)**n
        delta = 1
    else:
        delta = -1
    for i in range(n + 1):
        if (n - i) % 2 == 0:  # power = (-1)**(n - i)
            power_ = 1
        else:
            power_ = -1
        newcoefs[i] *= power_ * delta

    extremums.insert(0, -find_bound(newcoefs))

    roots = []
    for i in range(len(extremums) - 1):
        upper_bound = extremums[i + 1]
        lower_bound = extremums[i]
        mid_x = (upper_bound + lower_bound) / 2

        if f(lower_bound, coefs_) == 0:
            roots.append(lower_bound)
        elif f(upper_bound, coefs_) == 0:
            roots.append(upper_bound)
        else:
            middle = f(mid_x, coefs_)
            while middle != 0:
                # print(mid_x)
                if middle * f(upper_bound, coefs_) < 0:
                    lower_bound = mid_x
                else:
                    upper_bound = mid_x

                mid_x = (upper_bound + lower_bound) / 2
                middle = round(f(mid_x, coefs_), 4)
            roots.append(round(mid_x, 4))
    return roots


print('Введите коэфиценты: ', end='')
coefs = [float(a) for a in input().split()]

n = len(coefs) - 1
for coef in coefs:
    if coef == 0:
        n -= 1
    else:
        break

print('Степень полинома:', n)

print('Введенный многочлен f(x) = ', end='')
print_polinom(coefs)

print('Полученные корени:', *dichotomy(coefs))


# 1 -7 7 15 0 0 0
# 4 0 -95 75 226 -120
# 1 3 -14 -30 49 27 -36
