# -*- coding:utf-8 -*-
from threading import Thread

import psutil

try:
    # python3
    import urllib.request


    def fetch(urls):
        for url in urls:
            with urllib.request.urlopen(url) as r:
                r.read()
except ImportError:
    # python2
    import urllib


    def fetch(urls):
        for url in urls:
            r = urllib.urlopen(url)
            r.read()
            r.close()


def one_thread(tasks):
    fetch(tasks)


def two_threads(tasks):
    size = len(tasks)
    t1 = Thread(target=fetch, args=(tasks[:size // 2],))
    t2 = Thread(target=fetch, args=(tasks[size // 2:],))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def three_threads(tasks):
    size = len(tasks)
    t1 = Thread(target=fetch, args=(tasks[:size // 3],))
    t2 = Thread(target=fetch, args=(tasks[size // 3:2 * size // 3],))
    t3 = Thread(target=fetch, args=(tasks[2 * size // 3:],))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()


def four_threads(tasks):
    size = len(tasks)
    t1 = Thread(target=fetch, args=(tasks[:size // 4],))
    t2 = Thread(target=fetch, args=(tasks[size // 4:size // 2],))
    t3 = Thread(target=fetch, args=(tasks[size // 2:3 * size // 4],))
    t4 = Thread(target=fetch, args=(tasks[3 * size // 4:],))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()


def one_threads_1cpu(tasks):
    p = psutil.Process()
    p.cpu_affinity([1])
    one_thread(tasks)


def two_threads_1cpu(tasks):
    p = psutil.Process()
    p.cpu_affinity([1])
    two_threads(tasks)


def three_threads_1cpu(tasks):
    p = psutil.Process()
    p.cpu_affinity([1])
    three_threads(tasks)


def four_threads_1cpu(tasks):
    p = psutil.Process()
    p.cpu_affinity([1])
    four_threads(tasks)


if __name__ == '__main__':
    from utils.profile import TimeComparator

    # https://httpbin.org/
    # docker run -p 8080:80 kennethreitz/httpbin
    url = 'http://127.0.0.1:8080/delay/{delay}'.format(delay=0)
    urls = [url for i in range(12 * 100)]

    tc = TimeComparator()
    tc.compare(one_thread, two_threads, three_threads, four_threads,
               args=(urls,),
               python='python2.7',
               numbers=3)
    tc.compare(one_threads_1cpu, two_threads_1cpu, three_threads_1cpu,
               four_threads_1cpu,
               args=(urls,),
               python='python2.7',
               numbers=3)
    tc.compare(one_thread, two_threads, three_threads, four_threads,
               args=(urls,),
               numbers=3,
               python='python3.5')
    tc.compare(one_threads_1cpu, two_threads_1cpu, three_threads_1cpu,
               four_threads_1cpu,
               args=(urls,),
               python='python3.5',
               numbers=3)
