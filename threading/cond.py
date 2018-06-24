# 通过锁让两个线程交替执行，观察线程切换次数等

from threading import Thread, Condition

from utils import timeit_cm


def no_lock():
    init = 10 ** 5

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


def use_cond():
    init = 10 ** 5
    cond = Condition()

    def countdown(start, end):
        while end > start:
            with cond:
                end -= 1
                # 通知另一个，然后自身等待
                # 另一个唤醒自己，然后等待
                # 假若一个任务完成了，另一个则将进入挂起状态，所以可以在最后唤醒所有等待的
                # 也可以加入共享变量判断状态
                cond.notify()
                cond.wait()
        with cond:
            cond.notify()

    pw = Thread(target=countdown, args=(1, init))
    pr = Thread(target=countdown, args=(1, init))
    with timeit_cm():
        pw.start()
        pr.start()
        pw.join()
        pr.join()


if __name__ == '__main__':
    no_lock()
    use_cond()

    # : 0.02112412452697754
    # : 3.9102859497070312
