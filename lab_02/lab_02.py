from matplotlib import pyplot as plt
import xlrd


class Dot:
    def __init__(self, x, y, z, val):
        self.x = x
        self.y = y
        self.z = z
        self.val = val


class Buf_dot:
    def __init__(self, arg, val):
        self.arg = arg
        self.val = val


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
        if dot.arg < x:
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


def Newton_way(n, x, dots, printFl=0):
    start_ind, stop_ind = find_start_and_stop(n, x, dots)

    res = 0
    func_dict = {}
    for i in range(start_ind, stop_ind):
        func_dict[dots[i].arg] = dots[i].val

    if printFl:
        print(func_dict, start_ind, stop_ind)

    for i in range(start_ind, stop_ind):
        j = i - start_ind + 1
        args = []
        loc_sum = 1
        for k in range(j):
            args.append(dots[start_ind + k].arg)
            if k >= 1:
                loc_sum *= (x - dots[start_ind + k - 1].arg)
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


dots = []
dots_mtr = []
with open('data.txt') as f:
    z = 0
    line = f.readline()
    x_range = []
    string = []
    mtr = []
    while line:
        line = line.strip('\n')
        if 'z=' in line:
            if len(mtr):
                dots_mtr.append(mtr)
                mtr = []
            z = float(line.split('z=')[1])
        elif 'y\\x' not in line and len(line.split()) > 5:
            elems = line.split()
            for i in range(1, len(elems)):
                dots.append(Dot(float(x_range[i-1]), float(elems[0]), z, float(elems[i])))
                string.append(Dot(float(x_range[i - 1]), float(elems[0]), z, float(elems[i])))
        else:
            x_range = list(map(float, line.split()[1:]) if len(line.split()) > 5 else line.split())
        if len(string):
            mtr.append(string)
        string = []
        line = f.readline()
    if len(mtr):
        dots_mtr.append(mtr)

nx, ny, nz = list(map(int, input('Степени полиномов (nx, ny, nz) >> ').split()))
x, y, z = list(map(float, input('(x, y, z) >> ').split()))

vect_res = []
for k in range(len(dots_mtr)):
    vect = []
    for j in range(len(dots_mtr[k])):
        buf_dots = []
        for i in range(len(dots_mtr[k][j])):
            buf_dots.append(Buf_dot(dots_mtr[k][j][i].x, dots_mtr[k][j][i].val))
        vect.append(Newton_way(nx, x, buf_dots))
    buf_dots = []
    for j in range(len(dots_mtr[k])):
        buf_dots.append(Buf_dot(dots_mtr[k][j][0].y, vect[j]))
    vect_res.append(Newton_way(ny, y, buf_dots))

buf_dots = []
for k in range(len(dots_mtr)):
    buf_dots.append(Buf_dot(dots_mtr[k][0][0].z, vect_res[k]))

res = Newton_way(nz, z, buf_dots)
print(f'res = {res}')
