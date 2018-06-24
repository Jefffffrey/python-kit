from threading import Thread, Lock

from utils.threading import LockedIterator


def foo():
    for i in range(100000):
        yield i


lock = Lock()
count = 0

nums = foo()


def no_lock():
    def do():
        global count
        # Generator is not thread safe
        # ValueError: generator already executing
        for _ in nums:
            with lock:
                count += 1

    t1 = Thread(target=do)
    t2 = Thread(target=do)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


locked_nums = LockedIterator(foo())


def use_lock():
    def do():
        global count
        for _ in locked_nums:
            with lock:
                count += 1

    t1 = Thread(target=do)
    t2 = Thread(target=do)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    # use_lock()
    no_lock()
