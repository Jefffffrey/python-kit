# -*- coding:utf-8 -*-
# https://blog.csdn.net/HeatDeath/article/details/72844120
import os
from multiprocessing import Process, Queue

from utils import timeit_cm
from utils.faker_ import generate_tuple_list


def _timeit(length=100000):
    data = generate_tuple_list(length)

    def write(q):
        print('Process to write: %s' % os.getpid())
        for value in data:
            q.put(value)

    def read(q):
        print('Process to read: %s' % os.getpid())
        while True:
            q.get()

    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    with timeit_cm():
        pw.start()
        pr.start()
        pw.join()
        pr.terminate()


if __name__ == '__main__':
    _timeit(155000)
    _timeit(155000 * 2)
    _timeit(155000 * 3)

"""
Process to write: 23935
Process to read: 23937
: 5.8798394203186035
Process to write: 23988
Process to read: 23990
: 13.425143480300903
Process to write: 23994
Process to read: 23995
: 17.957948923110962
"""
