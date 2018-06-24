from threading import Thread, Lock

from utils import timeit_cm, pause


def no_lock():
    init = 10 ** 6

    def countdown(start, end):
        while end > start:
            end -= 1

    pw = Thread(target=countdown, args=(1, init))
    pr = Thread(target=countdown, args=(1, init))
    with timeit_cm():
        pw.start()
        pr.start()
        pw.join()
        pr.join()


def use_lock():
    init = 10 ** 5
    lock = Lock()

    def countdown(start, end):
        while end > start:
            with lock:
                end -= 1
        pause()

    pw = Thread(target=countdown, args=(1, init))
    pr = Thread(target=countdown, args=(1, init))
    with timeit_cm():
        pw.start()
        pr.start()
        pw.join()
        pr.join()


if __name__ == '__main__':
    # no_lock()
    pause()
    use_lock()
    pause()

    # 切换次数
    # 调用次数
