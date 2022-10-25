from multiprocessing import Pool
from solve import reseed,sa
if __name__ == '__main__':
    pool = Pool(processes=16)
    pool.map(reseed, range(16))
    pool.map(sa, range(16))
    pool.close()
    pool.join()
