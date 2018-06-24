# -*- coding:utf-8 -*-
import os
from collections import deque
from queue import Queue
from threading import Thread, Condition

import psutil

from utils import timeit_cm, timeit, pause
from utils.faker_ import generate_tuple_list


def use_queue(length=100000, maxsize=0):
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

    q = Queue(maxsize=maxsize)
    pw = Thread(target=write, args=(q,))
    pr = Thread(target=read, args=(q,))
    with timeit_cm():
        pw.start()
        pr.start()
        pw.join()
        pr.join()


def use_unlimited_deque_and_one_condition(length=100000):
    """
    生产者生产数据，消费者消费，消费者没有数据等待，每次生产者生产了数据都唤醒一次
    """
    data = generate_tuple_list(length)

    _not_end = True

    cond = Condition()

    def write(q):
        print('Process to write: %s' % os.getpid())
        for value in data:
            with cond:
                q.append(value)
                cond.notify()

        nonlocal _not_end
        _not_end = False

    def read(q):
        print('Process to read: %s' % os.getpid())

        while True:
            # 有数据
            if len(q):
                with cond:
                    q.popleft()
            # 没有数据
            elif _not_end:
                with cond:
                    cond.wait()
            # 结束
            else:
                break

    q = deque()
    pw = Thread(target=write, args=(q,))
    pr = Thread(target=read, args=(q,))
    with timeit_cm():
        pw.start()
        pr.start()
        pw.join()
        pr.join()


def use_limited_deque_and_one_condition(length=100000, max_size=1):
    """
    生产者队列满了等待，消费了唤醒：
        - 唤醒了生产者
        - 唤醒了消费者
    消费者没数据等待，消费了唤醒：
        - 唤醒了生产者
        - 唤醒了消费者
    """
    assert max_size > 0
    data = generate_tuple_list(length)

    _not_end = True

    cond = Condition()

    def write(q):
        print('Process to write: %s' % os.getpid())
        for value in data:
            with cond:
                if len(q) >= max_size:
                    # 等待在一个变量上，可能被消费者唤醒（多生产者的时候可能被生产者唤醒）
                    cond.wait()
                q.append(value)
                cond.notify()

        nonlocal _not_end
        _not_end = False

    def read(q):
        print('Process to read: %s' % os.getpid())

        while True:
            # 有数据
            if len(q):
                with cond:
                    q.popleft()
                    # 唤醒生产者，多消费者的时候可能唤醒消费者
                    cond.notify()

            # 没有数据
            elif _not_end:
                with cond:
                    cond.wait()
            # 结束
            else:
                break

    q = deque()
    pw = Thread(target=write, args=(q,))
    pr = Thread(target=read, args=(q,))
    with timeit_cm():
        pw.start()
        pr.start()
        pw.join()
        pr.join()


if __name__ == '__main__':
    # timeit(use_queue, (155000,))  # 2
    # timeit(use_queue, (155000, 1))  # 7
    # timeit(use_queue, (155000, 2))  # 5
    # timeit(use_queue, (155000, 3))  # 4
    # timeit(use_queue, (155000, 4))  # 3
    # timeit(use_queue, (155000, 10))  # 2.x
    # timeit(use_queue, (155000, 100))  # 2
    # timeit(use_queue, (155000, 1000))  # 2
    # timeit(use_queue, (155000 * 2,))
    # timeit(use_queue, (155000 * 3,))
    """
    155000    : 2.100769281387329
    155000 * 2: 4.206401824951172
    155000 * 3: 6.4216389656066895
    """
    # timeit(use_deque_and_one_condition, (155000 * 2,))  # 1.0
    p = psutil.Process()
    p.cpu_affinity([1])

    pause()
    # timeit(use_unlimited_deque_and_one_condition, (155000,))  # 4.1

    timeit(use_limited_deque_and_one_condition, (155000, 1))  # 6.7
    #  99.99    1.488000      106286        14           futex

    pause()
    # pause()
    # timeit(use_limited_deque_and_one_condition, (155000, 2))  # 4.1
    # timeit(use_limited_deque_and_one_condition, (155000, 3))  # 3.2
    # timeit(use_limited_deque_and_one_condition, (155000, 10))  # 1.8
    # timeit(use_limited_deque_and_one_condition, (155000, 100))  # 1.2
    # timeit(use_limited_deque_and_one_condition, (155000, 1000))  # 1.2
