import string
import random
import math
import qrcode
import numpy as np
import pyzbar.pyzbar as pyzbar
from PIL import Image

X, Y = 103, 137     # 马赛克左上角位置(单位为像素)
N = 20              # 马赛克块的数量（共N*N块）
BOX_SIZE = 23       # 每个马赛克块的大小（边长，单位为像素）
PIXEL_SIZE = 11     # 二维码每个块的大小（边长，单位为像素）
N_QR = 57


def random_string(n):
    '''生成长度为n的随机字符串'''
    letters = string.ascii_letters + string.digits
    return ''.join(random.choices(letters, k=n))


def pixelate(img):
    '''对图片的一部分打码，算法为取每块的平均值下取整'''
    ar = np.asarray(img, dtype='uint8')
    for i, j in np.ndindex(N, N):
        x1 = X + i*BOX_SIZE
        x2 = X + (i+1)*BOX_SIZE
        y1 = Y + j*BOX_SIZE
        y2 = Y + (j+1)*BOX_SIZE
        mean = math.floor(ar[x1:x2, y1:y2].mean())
        ar[x1:x2, y1:y2] = mean
    return Image.fromarray(ar, mode='L')


qr = np.zeros((N_QR, N_QR), dtype='int32')
qr.fill(-1)
data = None
visited = np.zeros((N, N), dtype='int32')
seq = []
good_choices_id = dict()

def no_to_coord(no):
    return no // N, no % N


def coord_to_no(x, y):
    return x*N + y


def next(x, y):
    return no_to_coord(seq[coord_to_no(x, y) + 1])


def finish(x, y):
    return visited[x, y] == 1


def dfs(id):
    global data
    global good_choices_id
    # print(id)
    x, y = no_to_coord(seq[id])
    print(x, y)
    if(finish(x, y)):
        return 1
    visited[x, y] = 1
    x_start = X + x*BOX_SIZE  # start x coordinate if this mosiac
    y_start = Y + y*BOX_SIZE  # start y coordinate if this mosiac

    x_no_start = x_start//PIXEL_SIZE  # start x index of covered block
    y_no_start = y_start//PIXEL_SIZE  # start y index of covered block
    good_choices = good_choices_id[coord_to_no(x, y)]
    back = np.copy(qr[x_no_start:x_no_start+3, y_no_start:y_no_start+3])
    if(len(good_choices)>=4): #fuck this
        return dfs(id+1)
    for choice in good_choices:
        qr[x_no_start:x_no_start+3, y_no_start:y_no_start+3] = back
        bad = 0
        for no in range(9):
            tx = x_no_start+no // 3
            ty = y_no_start+no % 3
            if(qr[tx][ty] == -1):
                qr[tx][ty] = ((choice >> no) & 1)
            elif qr[tx][ty] != ((choice >> no) & 1):
                bad = 1
                break
        if bad:
            continue
        if dfs(id+1) == 1:
            # visited[x, y] = 0
            return 1
    qr[x_no_start:x_no_start+3, y_no_start:y_no_start+3] = back
    visited[x, y] = 0
    return 0

def try_fix1():
    for x in range(20):
        for y in range(20):
            # print(id)
            x_start = X + x*BOX_SIZE  # start x coordinate if this mosiac
            y_start = Y + y*BOX_SIZE  # start y coordinate if this mosiac

            x_no_start = x_start//PIXEL_SIZE  # start x index of covered block
            y_no_start = y_start//PIXEL_SIZE  # start y index of covered block
            good_choices = good_choices_id[coord_to_no(x, y)]
            if len(good_choices) == 1:
                choice = good_choices[0]
                for no in range(9):
                    tx = x_no_start+no // 3
                    ty = y_no_start+no % 3
                    if(qr[tx][ty] == -1):
                        qr[tx][ty] = ((choice >> no) & 1)
    return 0

def try_fix2():
    for x in range(20):
        for y in range(20):
            # print(id)
            x_start = X + x*BOX_SIZE  # start x coordinate if this mosiac
            y_start = Y + y*BOX_SIZE  # start y coordinate if this mosiac

            x_no_start = x_start//PIXEL_SIZE  # start x index of covered block
            y_no_start = y_start//PIXEL_SIZE  # start y index of covered block
            good_choices = good_choices_id[coord_to_no(x, y)]
            back = np.copy(
                qr[x_no_start:x_no_start+3, y_no_start:y_no_start+3])
            if len(good_choices) >= 1:
                choice = good_choices[random.randint(0, len(good_choices)-1)]
                for no in range(9):
                    tx = x_no_start+no // 3
                    ty = y_no_start+no % 3
                    if(qr[tx][ty] == -1):
                        qr[tx][ty] = ((choice >> no) & 1)
    return 0


def try_fix3():
    valid = 0
    for x in range(20):
        for y in range(20):
            # print(id)
            x_start = X + x*BOX_SIZE  # start x coordinate if this mosiac
            y_start = Y + y*BOX_SIZE  # start y coordinate if this mosiac

            x_no_start = x_start//PIXEL_SIZE  # start x index of covered block
            y_no_start = y_start//PIXEL_SIZE  # start y index of covered block
            good_choices = good_choices_id[coord_to_no(x, y)]
            only_good_choice = -1
            is_only_good_choice = 0
            back = np.copy(
                qr[x_no_start:x_no_start+3, y_no_start:y_no_start+3])
            if len(good_choices) >= 1:
                for choice in good_choices:
                    qr[x_no_start:x_no_start+3, y_no_start:y_no_start+3] = back
                    bad = 0
                    for no in range(9):
                        tx = x_no_start+no // 3
                        ty = y_no_start+no % 3
                        if qr[tx][ty] != -1 and qr[tx][ty] != ((choice >> no) & 1):
                            bad = 1
                            break
                    if bad:
                        continue
                    if only_good_choice == -1:
                        is_only_good_choice = 1
                        only_good_choice = choice
                    else:
                        is_only_good_choice = 0
            if is_only_good_choice:
                for no in range(9):
                    tx = x_no_start+no // 3
                    ty = y_no_start+no % 3
                    if(qr[tx][ty] == -1):
                        valid = 1
                        qr[tx][ty] = ((only_good_choice >> no) & 1)

    return valid

def calc_good_choices():
    for x in range(20):
        for y in range(20):
            x_start = X + x*BOX_SIZE  # start x coordinate if this mosiac
            y_start = Y + y*BOX_SIZE  # start y coordinate if this mosiac
            color = data[x_start+1][y_start+1]  # mosiac color
            x_end = X + (x+1)*BOX_SIZE  # end x coordinate if this mosiac
            y_end = Y + (y+1)*BOX_SIZE  # end y coordinate if this mosiac

            x_no_start = x_start//PIXEL_SIZE  # start x index of covered block
            y_no_start = y_start//PIXEL_SIZE  # start y index of covered block

            # up unfully-covered block size in pixel
            lx = (x_no_start+1)*PIXEL_SIZE - x_start
            # left unfully-covered block size in pixel
            ly = (y_no_start+1)*PIXEL_SIZE - y_start

            # down unfully-covered block size in pixel
            hx = x_end - (x_no_start+2)*PIXEL_SIZE
            # right unfully-covered block size in pixel
            hy = y_end - (y_no_start+2)*PIXEL_SIZE

            # get the corresponding parameter and possible answer
            parameters = [lx*ly, lx*PIXEL_SIZE, lx*hy,
                        PIXEL_SIZE*ly, PIXEL_SIZE*PIXEL_SIZE, PIXEL_SIZE*hy,
                        hx*ly, hx*PIXEL_SIZE, hx*hy]

            good_choices = []
            for choice in range(0, 1 << 9):
                sum = 0
                conflict = 0
                for no in range(9):
                    tx = x_no_start+no // 3
                    ty = y_no_start+no % 3
                    if(qr[tx][ty] == -1):
                        if (choice >> no) & 1:
                            sum += parameters[no]*255
                    else:
                        if qr[tx][ty] != ((choice >> no) & 1):
                            conflict = 1
                            break
                        sum += parameters[no]*qr[tx][ty]*255
                if conflict:
                    continue
                if math.floor(sum/BOX_SIZE/BOX_SIZE) == color:
                    good_choices.append(choice)
            
            good_choices_id[coord_to_no(x, y)] = good_choices


def finding_pattern(x,y):
    for i in range(x-2,x+3):
        for j in range(y-2,y+3):
            qr[i][j] = 0 # black
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            qr[i][j] = 1  # white
    qr[x][y] = 0

if __name__ == '__main__':
    img = Image.open('./pixelated_qrcode.bmp')
    data = np.array(img)
    for i in range(627):
        for j in range(627):
            if data[i][j] == 0:
                qr[i//PIXEL_SIZE][j//PIXEL_SIZE] = 0
            elif data[i][j] == 255:
                qr[i//PIXEL_SIZE][j//PIXEL_SIZE] = 1

    finding_pattern(6,28)
    finding_pattern(28,6)
    finding_pattern(28,28)
    finding_pattern(28,50)
    finding_pattern(50,28)
    finding_pattern(50,50)
    calc_good_choices()
    try_fix1()
    seq = [x for x in range(400)]
    seq.append(399)
    # while len(res) == 0:
    #     qr = back.copy()
    #     # try_fix2()

    #     for i in range(627):
    #         for j in range(627):
    #             if qr[i//PIXEL_SIZE][j//PIXEL_SIZE] == -1:
    #                 data[i][j] = 80
    #             else:
    #                 data[i][j] = qr[i//PIXEL_SIZE][j//PIXEL_SIZE]*255
    #     res = pyzbar.decode(data)
    # print(res)
    valid = 1
    while valid:
        valid = try_fix3()

    dfs(0)
    
    for i in range(627):
        for j in range(627):
            if qr[i//PIXEL_SIZE][j//PIXEL_SIZE] == -1:
                data[i][j] = 80
            else:
                data[i][j] = qr[i//PIXEL_SIZE][j//PIXEL_SIZE]*255
    res = pyzbar.decode(data)
    print(res)
    Image.fromarray(data, mode='L').save('./qrcode_fixed.png')
