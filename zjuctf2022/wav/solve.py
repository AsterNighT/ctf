import array
from struct import pack, unpack
from functools import reduce
import librosa
import numpy as np

y, sr = librosa.load('./audio.wav', sr=None, mono=False)

lsb_num = 1
data_len = 64


def aug(x, y):
    return (x << lsb_num) + (unpack('i', pack('f', y))[0] & (2**lsb_num-1))


def get_lsbs(arr):
    x = 0
    return reduce(
        lambda x, y: aug(x, y),
        arr[:data_len],
        0).to_bytes(data_len//8, 'big')


def get_lsbs_zip(arr):
    x = 0
    return reduce(
        lambda x, y: aug(aug(x, y[0]), y[1]),
        arr,
        0).to_bytes(data_len//4, 'big')


zip(y[0][:data_len], y[1][:data_len])
print(get_lsbs_zip(zip(y[0][:data_len], y[1][:data_len])))
