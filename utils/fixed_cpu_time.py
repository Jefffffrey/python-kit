import time

from utils import timeit

__all__ = ['wait_cpu']


def _countdown(n):
    assert isinstance(n, int)
    while n:
        n -= 1


def wait_cpu(seconds):
    _countdown(int(18629271 * seconds))


def _one_second_n():
    n = 10 ** 8
    start = time.time()
    _countdown(n)
    end = time.time()
    print end - start
    return int(n / (end - start))


if __name__ == '__main__':
    timeit(_countdown, (18629271,))
    timeit(_countdown, (int(18629271 * 0.03),))

    timeit(wait_cpu, (2,))
    timeit(wait_cpu, (10,))

    _one_second_n()
