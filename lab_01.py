from matplotlib import pyplot as plt
import xlrd

# class Dot:
#     def __init__(self, x, y, dir):
#         self.x = x
#         self.y = y
#         self.dir = dir


book = xlrd.open_workbook("table.xls")
sh = book.sheet_by_index(0)

mtr = []
arg_func_dict = {}
for r in range(1, sh.nrows):
    row = []
    for c in range(sh.ncols):
        row.append(float(sh.cell_value(r, c)))
    mtr.append(row)
    arg_func_dict[row[0]] = row[1]

def mtr_sort(mtr):
    n = len(mtr)
    for i in range(n-1):
        flag = True
        for j in range(n-1-i):
            if mtr[j][0] > mtr[j + 1][0]:
                mtr[j], mtr[j + 1] = mtr[j + 1], mtr[j]
                flag = False
        if flag:
            break
    return mtr


mtr = mtr_sort(mtr)

x = []
y = []
print('\nОтсортированная таблица функции и ее производных:')
print('      x           y           y\'')
for row in mtr:
    x.append(row[0])
    y.append(row[1])
    for el in row:
        print(f'{el:^12.6f}', end='')
    print()

plt.plot(x, y)


def culc_func_for_newton(args, dictt):
    if len(args) == 1:
        return dictt[args[0]]
    if len(args) == 2:
        return (dictt[args[0]] - dictt[args[1]])/(args[0] - args[1])
    else:
        return (culc_func_for_newton(args[:-1], dictt) - culc_func_for_newton(args[1:], dictt)) / (args[0] - args[-1])

def culc_func_for_ermit(args, dictt):
    if len(args) == 1:
        return dictt[args[0]][0]
    if len(args) == 2 and args[0] != args[1]:
        return (dictt[args[0]][0] - dictt[args[1]][0])/(args[0] - args[1])
    elif len(args) == 2 and args[0] == args[1]:
        return dictt[args[0]][1]
    else:
        return (culc_func_for_ermit(args[:-1], dictt) - culc_func_for_ermit(args[1:], dictt)) / (args[0] - args[-1])


def Newton_way(n, x, table):
    if n + 1 > len(table):
        print('Недостаточно точек для заданного n!')
        exit(1)

    index = 0
    for row in table:
        if row[0] <= x:
            index += 1

    half1 = (n + 1) // 2
    half2 = (n + 1) - half1

    start_ind = (index - half1) if (index - half1 >= 0) else 0
    stop_ind = (index + half2) if (index + half2 <= len(table)) else len(table)

    if start_ind == 0:
        stop_ind += abs(index - half1)

    if stop_ind == len(table):
        start_ind -= index + half2 - len(table)

    res = 0
    func_dict = {}
    for i in range(start_ind, stop_ind):
        func_dict[table[i][0]] = table[i][1]

    for i in range(start_ind, stop_ind):
        j = i - start_ind + 1
        args = []
        loc_sum = 1
        for k in range(j):
            args.append(table[start_ind + k][0])
            if k >= 1:
                loc_sum *= (x - table[start_ind + k - 1][0])
        loc_sum *= culc_func_for_newton(args, func_dict)
        res += loc_sum

    return res

def Ermit_way(n, x, table):
    if n > len(table):
        print('Недостаточно точек для заданного n!')
        exit(1)

    index = 0
    for row in table:
        if row[0] <= x:
            index += 1

    half1 = n // 2
    half2 = n - half1

    start_ind = (index - half1) if (index - half1 >= 0) else 0
    stop_ind = (index + half2) if (index + half2 <= len(table)) else len(table)

    if start_ind == 0:
        stop_ind += abs(index - half1)

    if stop_ind == len(table):
        start_ind -= index + half2 - len(table)

    res = 0
    func_dict = {}
    for i in range(start_ind, stop_ind):
        func_dict[table[i][0]] = [table[i][1], table[i][2]]

    j = -1
    for i in range(start_ind, stop_ind):
        j += 2
        for ii in range(2):
            args = []
            loc_sum = 1
            for l in range(j + ii):
                k = l//2
                # if l % 2 != 0:
                #     k -= 1
                args.append(table[start_ind + k][0])
                if l >= 1:
                    loc_sum *= (x - table[start_ind + k][0])

            loc_sum *= culc_func_for_ermit(args, func_dict)
            res += loc_sum

    return res

def find_root(table, n=2):
    sw_table = []
    for i in range(len(table)):
        sw_table.append([table[i][1], table[i][0]])

    sw_table = mtr_sort(sw_table)
    root = Newton_way(n, 0, sw_table)
    return root

try:
    arg = float(input('\nЗначение x >> '))
except:
    print('Некорректный ввод')
    exit(1)

reses_n = []
print('\n         ', end='')
for i in range(1, 6):
    print(f'    n={i}    ', end='')
    reses_n.append(Newton_way(i, arg, mtr))

for i in range(len(reses_n)):
    reses_n[i] = f'{reses_n[i]:10.6f}'

print('\nНьютон:  ' + ' '.join(reses_n))


reses_e = []
print('\n         ', end='')
for i in range(1, 4):
    print(f'    n={i}    ', end='')
    reses_e.append(Ermit_way(i, arg, mtr))

for i in range(len(reses_e)):
    reses_e[i] = f'{reses_e[i]:10.6f}'

print('\nЕрмит:   ' + ' '.join(reses_e))


roots_n = []
print('\n         ', end='')
for i in range(1, 6):
    print(f'    n={i}    ', end='')
    roots_n.append(find_root(mtr, i))

for i in range(len(roots_n)):
    roots_n[i] = f'{roots_n[i]:10.6f}'

print('\nКорни:  ' + ' '.join(roots_n))


var = input('\nПолином Ньютона или Эрмита (n/e) >> ')
n = 0
e = 0

if var == 'n':
    try:
        n = int(input(f'Степень аппроксимирующего полинома Ньютона (от 1 до {len(mtr)-1}) >> '))
        if n < 1 or n > len(mtr)-1:
            print('Некорректный ввод')
            exit(1)
    except:
        print('Некорректный ввод')
        exit(1)
elif var == 'e':
    try:
        e = int(input(f'Кол-во узлов в полиноме Эрмита (от 1 до {len(mtr)}) >> '))
        if e < 1 or e > len(mtr):
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
    res = Newton_way(n, arg, mtr)
    root = find_root(mtr, n)
    print(f'result = {res}, root = {root}')
    plt.scatter(arg, res, c='blue')
    plt.scatter(root, 0, c='red')
    plt.show()
if e:
    res = Ermit_way(e, arg, mtr)
    root = find_root(mtr, e)
    print(f'result = {res}, root = {root}')
    plt.scatter(arg, res, c='blue')
    plt.scatter(root, 0, c='red')
    plt.show()