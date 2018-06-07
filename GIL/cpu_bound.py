# -*- coding:utf-8 -*-
from threading import Thread

import psutil


def countdown(start, end):
    while end > start:
        end -= 1


def one_thread(n):
    countdown(0, n)


def two_threads(n):
    t1 = Thread(target=countdown, args=(0, n // 2))
    t2 = Thread(target=countdown, args=(n // 2, n))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def three_threads(n):
    t1 = Thread(target=countdown, args=(0, n // 3))
    t2 = Thread(target=countdown, args=(n // 3, 2 * n // 3))
    t3 = Thread(target=countdown, args=(2 * n // 3, n))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()


def four_threads(n):
    t1 = Thread(target=countdown, args=(0, n // 4))
    t2 = Thread(target=countdown, args=(n // 4, n // 2))
    t3 = Thread(target=countdown, args=(n // 2, 3 * n // 4))
    t4 = Thread(target=countdown, args=(3 * n // 4, n))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()


def one_threads_1cpu(n):
    p = psutil.Process()
    p.cpu_affinity([1])
    one_thread(n)


def two_threads_1cpu(n):
    p = psutil.Process()
    p.cpu_affinity([1])
    two_threads(n)


def three_threads_1cpu(n):
    p = psutil.Process()
    p.cpu_affinity([1])
    three_threads(n)


def four_threads_1cpu(n):
    p = psutil.Process()
    p.cpu_affinity([1])
    four_threads(n)


if __name__ == '__main__':
    from utils.profile import TimeComparator

    tc = TimeComparator()
    tc.compare(one_thread, two_threads, three_threads, four_threads,
               args=(12 * 10 ** 7,),
               numbers=10,
               python='python2.7')
    tc.compare(one_threads_1cpu, two_threads_1cpu, three_threads_1cpu,
               four_threads_1cpu,
               args=(12 * 10 ** 7,),
               python='python2.7',
               numbers=10)
    tc.compare(one_thread, two_threads, three_threads, four_threads,
               args=(12 * 10 ** 7,),
               numbers=10,
               python='python3.5')
    tc.compare(one_threads_1cpu, two_threads_1cpu, three_threads_1cpu,
               four_threads_1cpu,
               args=(12 * 10 ** 7,),
               python='python3.5',
               numbers=10)
