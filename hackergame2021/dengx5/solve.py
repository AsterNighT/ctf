from multiprocessing import Pool
import copy
import win32api
import win32con
import numpy
import random
import math
from sko.GA import GA


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def gcd(a, b):
    """
    Return the greatest common denominator of integers a and b.
    gmpy2.gcd(a, b)
    """
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b / (gcd(a, b))


def egcd(a, b):
    """
    ax + by = 1
    ax ≡ 1 mod b
    Return a 3-element tuple (g, x, y), the g  = gcd(a, b)
    gmpy2.gcdext(a, b)
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def mod_inv(a, m):
    """
    ax ≡ 1 mod m
    gmpy2.invert(a, m)
    """
    g, x, y = egcd(a, m)
    assert g == 1
    return x % m


def int2mem(x):
    """
    0x12233 => '\x33\x22\x01'
    """
    def pad_even(x): return ('', '0')[len(x) % 2] + x
    x = list(pad_even(format(x, 'x')).decode('hex'))
    x.reverse()
    return ''.join(x)


def mem2int(x):
    """
    '\x33\x22\x01' => 0x12233
    """
    x = list(x)
    x.reverse()
    return int(''.join(x).encode('hex'), 16)

###########################################################
# class
###########################################################


class GaussMatrix:
    """
    A*X ≡ B (mod p),p为大于0的整数。

    高斯消元求解模线性方程组。先化简为上三角，然后回代求解。
    当r(A) <= n时，一定有多解；
    当r(A) == n时，有多解或唯一解；
    当r(A) != r(A~)时，无解。
    r(A)为系数矩阵的秩，r(A)为增广矩阵的秩，n为未知数的个数。

    http://www.docin.com/p-1063811671.html讨论了gcd(|A|, m) = 1时的LU分解解法，
    本文包括了gcd(|A|, m) > 1时的解法，

    化简原则：
        1、系数与模互质
        2、系数加某一行n次后，对应的系数与模的GCD最小
        3、将1或2得到的系数移到对角线上

    初始化参数：
        matrix：方程组的增广矩阵（最后一列为常数项）。
            matrix = [
                [ 69,  75,  78,  36,  58],
                [ 46,  68,  51,  26,  42],
                [ 76,  40,  42,  49,  11],
                [ 11,  45,   2,  45,   1],
                [ 15,  67,  60,  14,  72],
                [ 76,  67,  73,  56,  58],
                [ 67,  15,  68,  54,  75],
            ]    
        mod：模数

    函数：
        gauss()：求解方程

    输出变量：
        error_str：出错的信息
        count：解的数量
    """

    def __init__(self, matrix, mod):
        self.matrix = copy.deepcopy(matrix)
        self.d = None

        self.r = len(matrix)
        self.c = len(matrix[0])
        self.N = len(matrix[0]) - 1
        self.mod = mod
        self.count = 1
        self.error_str = "unknown error"

    def verify_solution(self, solution):
        for d in self.matrix:
            result = 0
            for r in map(lambda x, y: 0 if None == y else x*y, d, solution):
                result += r
            if (result % self.mod) != ((d[-1]) % self.mod):
                return 0
        return 1

    def swap_row(self, ra, rb):
        (self.d[ra], self.d[rb]) = (self.d[rb], self.d[ra])

    def swap_col(self, ca, cb):
        for j in range(self.r):
            (self.d[j][ca], self.d[j][cb]) = (self.d[j][cb], self.d[j][ca])

    def inv_result(self, r, n):
        """
        求解第n个未知数，r已经获得的解。形如：[None,None, ..., n+1, ...]

        a*x ≡ b(mod m)
        x有解的条件：gcd(a,m) | b。也即a,m互质时一定有解，不互质时，b整除gcd(a,m)也有解，否则无解。
        解的格式为：x0+k(m/gcd(a,m))，其中x0为最小整数特解，k为任意整数。
        返回[x0, x1, ...xn]，其中x0 < x1 < xn < m。
        """
        b = self.d[n][self.N]
        a = self.d[n][n]
        m = self.mod
        k = gcd(a, m)
        for j in range(n + 1, self.N):
            b = (b - (self.d[n][j] * r[j] % m)) % m

        if 1 == k:
            return [mod_inv(a, m) * b % m]
        else:
            if k == gcd(k, b):
                a /= k
                b /= k
                m /= k

                x0 = mod_inv(a, m) * b % m
                x = []
                for i in range(k):
                    x.append(x0 + m*i)
                return x
        return None

    def find_min_gcd_row_col(self, i, j):
        # 查找直接互质的对角线系数
        for k in range(i, self.r):
            for l in range(j, self.c - 1):
                if(1 == gcd(self.d[k][l], self.mod)):
                    return [k, l]

        def add_min_gcd(a, b, m):
            r = [m, 1]
            g = gcd(a, b)
            if g:
                i = a / g
                for j in range(i):
                    g = gcd((a + j * b) % m, m)
                    if g < r[0]:
                        r[0] = g
                        r[1] = j
                    if g == 1:
                        break
            return r

        # 查找加乘后GCD最小的对角线系数
        #   [加乘后的最大公约数,加乘的倍数,要化简的行号,加乘的行号,要化简的列号]
        r = [self.mod, 1, i, i + 1, j]
        for k in range(i, self.r):
            for kk in range(k+1, self.r):
                for l in range(j, self.c - 1):
                    rr = add_min_gcd(self.d[k][l], self.d[kk][l], self.mod)
                    if rr[0] < r[0]:
                        r[0] = rr[0]
                        r[1] = rr[1]
                        r[2] = k
                        r[3] = kk
                        r[4] = l
                        pass
                    if(1 == rr[0]):
                        break
        g = r[0]
        n = r[1]
        k = r[2]
        kk = r[3]
        l = r[4]

        if n and g < self.mod:
            self.d[k] = list(map(lambda x, y: (x + n*y) %
                                 self.mod, self.d[k], self.d[kk]))
        return [k, l]

    def mul_row(self, i, k, j):
        a = self.d[k][j]
        b = self.d[i][j]

        def get_mul(a, b, m):
            k = gcd(a, m)
            if 1 == k:
                return mod_inv(a, m) * b % m
            else:
                if k == gcd(k, b):
                    return mod_inv(a/k, m/k) * (b/k) % (m/k)
            return None

        if b:
            mul = get_mul(a, b, self.mod)
            if None == mul:
                print_matrix(self.d)
                assert(mul != None)
            self.d[i] = list(map(lambda x, y: (y - x*mul) %
                                 self.mod, self.d[k], self.d[i]))

    def gauss(self):
        """
        返回解向量，唯一解、多解或无解(None)。
        例如：[[61, 25, 116, 164], [61, 60, 116, 94], [61, 95, 116, 24], [61, 130, 116, 129], [61, 165, 116, 59]]
        """

        self.d = copy.deepcopy(self.matrix)
        for i in range(self.r):
            for j in range(self.c):
                self.d[i][j] = self.matrix[i][j] % self.mod  # 把负系数变成正系数

        if self.r < self.N:
            self.d.extend([[0]*self.c]*(self.N - self.r))

        # 化简上三角
        index = [x for x in range(self.N)]
        for i in range(self.N):
            tmp = self.find_min_gcd_row_col(i, i)
            if(tmp):
                self.swap_row(i, tmp[0])
                (index[i], index[tmp[1]]) = (index[tmp[1]], index[i])
                self.swap_col(i, tmp[1])
            else:
                self.error_str = "no min"
                return None

            for k in range(i + 1, self.r):
                self.mul_row(k, i, i)

        # print_matrix(self.d)
        if self.r > self.N:
            for i in range(self.N, self.r):
                for j in range(self.c):
                    if self.d[i][j]:
                        self.error_str = "r(A) != r(A~)"
                        return None

        # 判断解的数量
        for i in range(self.N):
            self.count *= gcd(self.d[i][i], self.mod)

        if self.count > 100:
            self.error_str = "solution too more:%d" % (self.count)
            return None

        # 回代
        result = [[None]*self.N]
        for i in range(self.N - 1, -1, -1):
            new_result = []
            for r in result:
                ret = self.inv_result(r, i)
                if ret:
                    for rr in ret:
                        l = r[:]
                        l[i] = rr
                        new_result.append(l)

                else:
                    self.error_str = "no inv:i=%d" % (i)
                    return None

            result = new_result
        final = [0]*size*size
        # 调整列变换导致的未知数顺序变化
        for i in range(len(index)):
            final[index[i]] = result[0][i]

        return final

###########################################################
# test
###########################################################


def print_array(x):
    prn = "\t["
    for j in x:
        if j:
            prn += "%d, " % j
        else:
            prn += "0, "

    print(prn[:-2]+"],")


def print_matrix(x):
    print("[")
    for i in x:
        print_array(i)
    print("]")


size = 12
directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]


def to_id(i, j):
    if(i < 0 or i >= size or j < 0 or j >= size):
        return -1
    return i*size+j


def gauss(target):
    matrix = []
    for i in range(size):
        for j in range(size):
            line = [0]*size*size
            for r in range(3):
                for d in directions:
                    x = i+d[0]*r
                    y = j+d[1]*r
                    id = to_id(x, y)
                    if id >= 0:
                        line[id] = 3-r
            line.append(target[i][j])
            matrix.append(line)
    # print_matrix(matrix)
    t = GaussMatrix(matrix, 256)
    ans = t.gauss()
    print(t.verify_solution(ans))
    print("Ans:")
    ret = []
    for i in range(size):
        ret.append(ans[i*size:i*size+size])
    print(ans)
    return ret


def do_click(ans):
    base_x = 3197
    base_y = 276
    target_x = 3838
    target_y = 916
    for i in range(size):
        for j in range(size):
            for _ in range(ans[i][j]):
                x = int(base_x + (target_x-base_x)*j/11)
                y = int(base_y + (target_y-base_y)*i/11)
                click(x, y)


def get_curser():
    print(win32api.GetCursorPos())


target = numpy.array([
    [189, 189, 189, 189, 189, 33, 33, 33, 189, 189, 189, 189],
    [189, 189, 189, 33, 33, 33, 189, 33, 44, 189, 189, 189],
    [189, 189, 189, 189, 189, 33, 33, 33, 33, 189, 189, 189],
    [189, 189, 189, 189, 189, 33, 189, 33, 33, 189, 189, 189],
    [189, 189, 189, 33, 33, 189, 189, 33, 33, 33, 189, 189],
    [189, 134, 33, 33, 189, 189, 189, 189, 33, 33, 189, 189],
    [189, 144, 33, 33, 189, 189, 189, 189, 33, 189, 189, 189],
    [189, 142, 33, 33, 189, 189, 189, 189, 33, 33, 33, 189],
    [189, 100, 142, 33, 189, 189, 189, 189, 33, 33, 33, 189],
    [189, 142, 142, 189, 189, 189, 189, 189, 189, 33, 189, 189],
    [189, 59, 142, 33, 189, 189, 189, 189, 33, 189, 189, 189],
    [189, 189, 33, 33, 189, 189, 189, 189, 189, 189, 189, 189]])
limit1 = numpy.array([
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]])
limit2 = numpy.array([
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]])


def get_cost1(click_matrix):
    click_matrix = click_matrix.reshape(12, 12)
    radius_map = [[0]*size]*size
    cost = -400
    for i in range(size):
        for j in range(size):
            if(numpy.isnan(click_matrix[i][j])):
                continue
            # if click_matrix[i][j] >= 256:
            #     return 99999999  # No way to go this far
            radius_map[i][j] += 3*click_matrix[i][j]
            for r in range(1, 3):
                for d in directions:
                    x = i+d[0]*r
                    y = j+d[1]*r
                    if(to_id(x, y) >= 0):  # inbound
                        radius_map[x][y] += (3-r)*click_matrix[i][j]
    for i in range(size):
        for j in range(size):
            radius_map[i][j] %= 256
            cost += abs(target[i][j]-radius_map[i][j])
    return cost


def greed():
    click_matrix = numpy.random.randint(0, 256, size=(size, size))
    click_matrix = numpy.minimum(click_matrix, limit1)
    click_matrix = click_matrix.reshape(size*size)
    print(get_cost1(click_matrix))
    while True:
        # calculate y
        cost0 = get_cost1(click_matrix)
        # generate a new x in the neighboorhood of x by transform function
        new_matrix = click_matrix.copy()
        while True:
            pos = random.randint(0, size*size-1)
            dir = -1**(random.randint(0, 1))
            if new_matrix[pos] == 0:
                dir = 1
            if new_matrix[pos] == 255:
                dir = -1
            if new_matrix[pos] + dir >= 0 and new_matrix[pos] + dir <= limit1[pos//size][pos % size]:
                new_matrix[pos] += dir
                break
        cost1 = get_cost1(new_matrix)
        if (cost0 > cost1):
            if(cost0-cost1 > 12):
                print("wtf?")
            click_matrix = new_matrix
            print(cost1)
    return click_matrix


def sa(_):
    click_matrix = numpy.random.randint(0, 256, size=(size, size))
    click_matrix = numpy.minimum(click_matrix, limit1)
    click_matrix = click_matrix.reshape(size*size)
    print(get_cost1(click_matrix))
    T0 = 100
    Tmin = 0.9
    k = 50
    t = 0
    T = T0
    cost0 = get_cost1(click_matrix)
    while T >= Tmin:
        for _ in range(k):
            # calculate y
            # generate a new x in the neighboorhood of x by transform function
            new_matrix = click_matrix.copy()
            pos = random.randint(0, size*size-1)
            new_matrix[pos] = random.randint(0, limit1[pos//size][pos % size])
            cost1 = get_cost1(new_matrix)
            if (cost0 > cost1):
                click_matrix = new_matrix
                cost0 = cost1
            else:
                # metropolis principle
                p = math.exp(-(cost1-cost0)/T)
                r = numpy.random.uniform(low=0, high=1)
                if r < p:
                    click_matrix = new_matrix
                    cost0 = cost1
        t += 1
        # print(t)
        T *= 0.999999
    with open('lights_up_result.txt', 'a') as f:
        print(cost0, file=f)
        print(repr(click_matrix), file=f)
        print(file=f)


def reseed(i):
    random.seed()



