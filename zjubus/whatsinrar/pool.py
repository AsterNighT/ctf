from multiprocessing import Pool
from run import test
if __name__ == '__main__':
    pool = Pool(4)
    pool.map(test,range(123465,123466))
