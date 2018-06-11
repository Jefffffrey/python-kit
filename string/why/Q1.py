import contextlib
import time


@contextlib.contextmanager
def timeit():
    start = time.time()
    yield
    end = time.time()
    print(end - start)


def str_plus_equal(num):
    s = ''
    for i in range(num):
        s += 'string'
    return s


def bytes_plus_equal(num):
    s = b''
    for i in range(num):
        s += b'string'
    return s


# if uncomment this block,bytes_plus_equal will be faster
with timeit():
    str_plus_equal(100000)

with timeit():
    bytes_plus_equal(100000)

# Comment:
# 7.781214714050293
# Uncomment str_plus_equal:
# 0.013445854187011719
# 4.366648197174072
