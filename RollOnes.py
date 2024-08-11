import datetime

import numpy
from numpy.random import randint

roll_sessions = 1000000
result = 0

d1 = datetime.datetime.now()
for _ in range(0, roll_sessions):
    rolled_array = randint(1, 5, size=231)
    numbers_of_rolled_ones = numpy.count_nonzero(rolled_array == 1)

    if result < numbers_of_rolled_ones:
        result = numbers_of_rolled_ones

d2 = datetime.datetime.now()

print(f"Highest Ones Roll: {result}")
print(f"Number of Roll Sessions: {roll_sessions}")
print(f"Time taken: {d2 - d1}")
