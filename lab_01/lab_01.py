from matplotlib import pyplot as plt
import xlrd

class Dot:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir


def culc_func_for_newton(args, dictt):
    if len(args) == 1:
        return dictt[args[0]]
    if len(args) == 2:
        return (dictt[args[0]] - dictt[args[1]]) / (args[0] - args[1])
    else:
        return (culc_func_for_newton(args[:-1], dictt) - culc_func_for_newton(args[1:], dictt)) / (args[0] - args[-1])


def culc_func_for_ermit(args, dictt):
    if len(args) == 1:
        return dictt[args[0]][0]
    if len(args) == 2 and args[0] != args[1]:
        return (dictt[args[0]][0] - dictt[args[1]][0]) / (args[0] - args[1])
    elif len(args) == 2 and args[0] == args[1]:
        return dictt[args[0]][1]
    else:
        return (culc_func_for_ermit(args[:-1], dictt) - culc_func_for_ermit(args[1:], dictt)) / (args[0] - args[-1])


def find_start_and_stop(n, x, dots):
    if n + 1 > len(dots):
        print('Недостаточно точек для заданного n!')
        exit(1)

    index = 0
    for dot in dots:
        if dot.x <= x:
            index += 1

    half1 = (n + 1) // 2
    half2 = (n + 1) - half1

    start_ind = (index - half1) if (index - half1 >= 0) else 0
    stop_ind = (index + half2) if (index + half2 <= len(dots)) else len(dots)

    if start_ind == 0:
        stop_ind += abs(index - half1)

    if stop_ind == len(dots):
        start_ind -= index + half2 - len(dots)

    return start_ind, stop_ind


def Newton_way(n, x, dots):
    start_ind, stop_ind = find_start_and_stop(n, x, dots)

    res = 0
    func_dict = {}
    for i in range(start_ind, stop_ind):
        func_dict[dots[i].x] = dots[i].y

    for i in range(start_ind, stop_ind):
        j = i - start_ind + 1
        args = []
        loc_sum = 1
        for k in range(j):
            args.append(dots[start_ind + k].x)
            if k >= 1:
                loc_sum *= (x - dots[start_ind + k - 1].x)
        loc_sum *= culc_func_for_newton(args, func_dict)
        res += loc_sum

    return res


def Ermit_way(n, x, dots):
    start_ind, stop_ind = find_start_and_stop(n, x, dots)

    res = 0
    func_dict = {}
    for i in range(start_ind, stop_ind):
        func_dict[dots[i].x] = [dots[i].y, dots[i].dir]

    j = -1
    for i in range(start_ind, stop_ind):
        j += 2
        for ii in range(2):
            args = []
            loc_sum = 1
            for l in range(j + ii):
                k = l // 2
                args.append(dots[start_ind + k].x)
                if l >= 1:
                    loc_sum *= (x - dots[start_ind + k].x)

            loc_sum *= culc_func_for_ermit(args, func_dict)
            res += loc_sum

    return res


def dots_sort(dots):
    n = len(dots)
    for i in range(n-1):
        flag = True
        for j in range(n-1-i):
            if dots[j].x > dots[j + 1].x:
                dots[j], dots[j + 1] = dots[j + 1], dots[j]
                flag = False
        if flag:
            break
    return dots


book = xlrd.open_workbook("table.xls")
sh = book.sheet_by_index(0)

dots = []
inverted_dots = []
arg_func_dict = {}
for r in range(1, sh.nrows):
    dot = []
    for c in range(sh.ncols):
        dot.append(float(sh.cell_value(r, c)))
    dots.append(Dot(dot[0], dot[1], dot[2]))
    inverted_dots.append(Dot(dot[1], dot[0], 1/dot[2]))
    arg_func_dict[dot[0]] = dot[1]


dots = dots_sort(dots)

x = []
y = []
print('\nОтсортированная таблица функции и ее производных:')
print('      x           y           y\'')
for dot in dots:
    x.append(dot.x)
    y.append(dot.y)
    print(f'{dot.x:^12.6f}', end='')
    print(f'{dot.y:^12.6f}', end='')
    print(f'{dot.dir:^12.6f}', end='')
    print()

plt.plot(x, y)

try:
    arg = float(input('\nЗначение x >> '))
except:
    print('Некорректный ввод')
    exit(1)

reses_n = []
print('\n         ', end='')
for i in range(1, 6):
    print(f'    n={i}    ', end='')
    reses_n.append(Newton_way(i, arg, dots))

for i in range(len(reses_n)):
    reses_n[i] = f'{reses_n[i]:10.6f}'

print('\nНьютон:  ' + ' '.join(reses_n))


reses_e = []
print('\n         ', end='')
for i in range(1, 4):
    print(f'    n={i}    ', end='')
    reses_e.append(Ermit_way(i, arg, dots))

for i in range(len(reses_e)):
    reses_e[i] = f'{reses_e[i]:10.6f}'

print('\nЕрмит:   ' + ' '.join(reses_e))


roots_n = []
print('\n         ', end='')
for i in range(1, 6):
    print(f'    n={i}    ', end='')
    roots_n.append(Newton_way(i, 0, inverted_dots))

for i in range(len(roots_n)):
    roots_n[i] = f'{roots_n[i]:10.6f}'

print('\nКорни:  ' + ' '.join(roots_n))


view = input('\nПросмотреть 1 решение? (y/n) >> ')

if view != 'y':
    exit(0)

var = input('\nПолином Ньютона или Эрмита (n/e) >> ')
n = 0
e = 0

if var == 'n':
    try:
        n = int(input(f'Степень аппроксимирующего полинома Ньютона (от 1 до {len(dots) - 1}) >> '))
        if n < 1 or n > len(dots)-1:
            print('Некорректный ввод')
            exit(1)
    except:
        print('Некорректный ввод')
        exit(1)
elif var == 'e':
    try:
        e = int(input(f'Кол-во узлов в полиноме Эрмита (от 1 до {len(dots)}) >> '))
        if e < 1 or e > len(dots):
            print('Некорректный ввод')
            exit(1)
    except:
        print('Некорректный ввод')
        exit(1)
else:
    print('Некорректный ввод')
    exit(1)

plt.grid()
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')

if n:
    res = Newton_way(n, arg, dots)
    root = Newton_way(n, 0, inverted_dots)
    print(f'result = {res}, root = {root}')
    plt.scatter(arg, res, c='blue')
    plt.scatter(root, 0, c='red')
    plt.show()
if e:
    res = Ermit_way(e, arg, dots)
    root = Newton_way(e, 0, inverted_dots)
    print(f'result = {res}, root = {root}')
    plt.scatter(arg, res, c='blue')
    plt.scatter(root, 0, c='red')
    plt.show()