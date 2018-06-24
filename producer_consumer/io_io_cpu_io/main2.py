# -*- coding:utf-8 -*-
"""
main.py的多进程＋多线程版本
"""
import urllib
from multiprocessing import Process
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
    for _ in range(25):
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


class Step12(Step):
    def _run(self, task):
        print 'task12'
        global urls
        print 'task1'
        for url in urls:
            fetch(url)
            fetch('http://127.0.0.1:8080/delay/{delay}'.format(delay=3))
            yield url


def _test():
    step1 = Step1(threads=3)
    step2 = Step2(threads=3)
    step3 = Step3(threads=1)
    step4 = Step4(threads=2)

    task = Task(steps=[step1, step2, step3, step4], queue_sizes=[3, 2, 2])
    task.start()
    task.join()


def test():
    # 电脑上运行后发现只要是2个以上，就在60s左右,也就是原来的一半，应该是系统的物理CPU只有2个，
    # 然后观察top发现，每个具体的进程CPU100%，然后整个系统分别是25 50 75 100,100和50是
    # 差不多的感觉，应该是用了超线程技术少了一些开销．但是其实不多＝．＝．总之设置为CPU核数
    # 就可以了

    # 修改进程数量的时候记得修改_test中url的个数
    p1 = Process(target=_test)
    p1.start()
    p2 = Process(target=_test)
    p2.start()
    p3 = Process(target=_test)
    p3.start()
    p4 = Process(target=_test)
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()


if __name__ == '__main__':
    with timeit_cm():
        test()
        # test2()
