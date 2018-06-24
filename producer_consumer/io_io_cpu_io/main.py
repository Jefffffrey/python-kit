# -*- coding:utf-8 -*-
"""
多线程版本．

任务流程为：IO,IO，CPU，IO
执行耗时为 2,3,1,2

test:
    3 3 1 2
     3 3 2 
test2:
    5 1 2
     5 2  
"""

import urllib
from threading import Lock

from task import *
from utils import timeit_cm
from utils.fixed_cpu_time import wait_cpu
from utils.threading import LockedIterator


def fetch(url):
    r = urllib.urlopen(url)
    r.read()
    r.close()


lock = Lock()


def urls():
    url = 'http://127.0.0.1:8080/delay/{delay}'.format(delay=2)
    for _ in range(100):
        yield url


urls = LockedIterator(urls())


class Step1(Step):
    def _run(self, task):
        global urls
        print 'task1'
        for url in urls:
            fetch(url)
            yield url


class Step2(Step):
    def _run(self, task):
        print 'task2'
        url = 'http://127.0.0.1:8080/delay/{delay}'.format(delay=3)
        fetch(url)
        return url


class Step3(Step):
    def _run(self, task):
        print 'task3'
        wait_cpu(1)
        return ''


class Step4(Step):
    def _run(self, task):
        print 'task4'
        url = 'http://127.0.0.1:8080/delay/{delay}'.format(delay=2)
        fetch(url)


def test():
    step1 = Step1(threads=3)
    step2 = Step2(threads=3)
    step3 = Step3(threads=1)
    step4 = Step4(threads=2)

    task = Task(steps=[step1, step2, step3, step4], queue_sizes=[3, 2, 2])
    task.start()
    task.join()


class Step12(Step):
    def _run(self, task):
        print 'task12'
        global urls
        for url in urls:
            fetch(url)
            fetch('http://127.0.0.1:8080/delay/{delay}'.format(delay=3))
            yield url


def test2():
    step12 = Step12(threads=5)
    step3 = Step3(threads=1)
    step4 = Step4(threads=2)

    task = Task(steps=[step12, step3, step4], queue_sizes=[2, 2])
    task.start()
    task.join()


if __name__ == '__main__':
    with timeit_cm():
        test()
        # test2()
