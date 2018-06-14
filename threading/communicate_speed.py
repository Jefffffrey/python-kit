# -*- coding:utf-8 -*-
# https://blog.csdn.net/HeatDeath/article/details/72844120
import os
from queue import Queue
from threading import Thread

from utils import timeit_cm
from utils.faker_ import generate_tuple_list


def _timeit(length=100000):
    data = generate_tuple_list(length)

    _not_end = True

    def write(q):
        print('Process to write: %s' % os.getpid())
        for value in data:
            q.put(value)
        nonlocal _not_end
        _not_end = False

    def read(q):
        print('Process to read: %s' % os.getpid())
        while q.qsize() or _not_end:
            q.get()

    q = Queue()
    pw = Thread(target=write, args=(q,))
    pr = Thread(target=read, args=(q,))
    with timeit_cm():
        pw.start()
        pr.start()
        pw.join()
        pr.join()


if __name__ == '__main__':
    _timeit(155000)
    _timeit(155000 * 2)
    _timeit(155000 * 3)


"""
Process to write: 24024
Process to read: 24024
: 2.100769281387329
Process to write: 24024
Process to read: 24024
: 4.206401824951172
Process to write: 24024
Process to read: 24024
: 6.4216389656066895
"""
