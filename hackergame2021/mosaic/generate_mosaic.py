import string
import random
import math
import qrcode
import numpy as np
from PIL import Image

X, Y = 103, 137     # 马赛克左上角位置(单位为像素)
N = 20              # 马赛克块的数量（共N*N块）
BOX_SIZE = 23       # 每个马赛克块的大小（边长，单位为像素）
PIXEL_SIZE = 11     # 二维码每个块的大小（边长，单位为像素）

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



if __name__ == '__main__':
    with open('flag.txt', 'r') as f:
        flag = f.read()
    qr = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=PIXEL_SIZE,
        border=0,
    )
    qr.add_data(random_string(30) + '__' + flag + '__' + random_string(30))
    img = qr.make_image(fill_color="black", back_color="white").convert('L')
    mosaic = pixelate(img)
    mosaic.save('mosaic.bmp')
