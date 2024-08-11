import datetime
import multiprocessing

import numpy
from numpy.random import randint


roll_sessions = 1000000


def worker(lock: multiprocessing.Lock, res: multiprocessing.Value('i')):
    result = 0
    for _ in range(0, roll_sessions):
        rolled_array = randint(1, 5, size=231)
        numbers_of_rolled_ones = numpy.count_nonzero(rolled_array == 1)

        if result < numbers_of_rolled_ones:
            result = numbers_of_rolled_ones

    with lock:
        if result > res.value:
            res.value = result


if __name__ == '__main__':
    jobs = []
    num_threads = 10
    res = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()
    d1 = datetime.datetime.now()

    for i in range(num_threads):
        p = multiprocessing.Process(target=worker, args=(lock, res))
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()

    d2 = datetime.datetime.now()

    print(f"Highest Ones Roll: {res.value}")
    print(f"Number of Roll Sessions: {roll_sessions*num_threads}")
    print(f"Time taken: {d2 - d1}")
