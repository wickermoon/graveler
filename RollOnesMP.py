import datetime
import locale
import multiprocessing

import numpy
from numpy.random import randint


def worker(tries: int, res: multiprocessing.Value('i')):
    result = 0
    for _ in range(0, tries):
        rolled_array = randint(1, 5, size=231)
        numbers_of_rolled_ones = numpy.count_nonzero(rolled_array == 1)

        if result < numbers_of_rolled_ones:
            result = numbers_of_rolled_ones

    if result > res.value:
        res.value = result


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    num_threads = 10
    tries = 100000000
    res = multiprocessing.Value('i', 0)
    print(f"Number of Roll Sessions: {tries * num_threads:n}")

    d1 = datetime.datetime.now()
    print(d1)

    jobs = [multiprocessing.Process(target=worker, args=(tries, res)) for _ in range(num_threads)]

    for job in jobs:
        job.start()

    for job in jobs:
        job.join()

    d2 = datetime.datetime.now()

    print(f"Highest Ones Roll: {res.value}")
    print(f"Time taken: {d2 - d1}")
