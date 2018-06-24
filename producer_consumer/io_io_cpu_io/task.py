# -*- coding:utf-8 -*-
from __future__ import absolute_import

from Queue import Queue
from threading import Thread


class Step(object):
    def __init__(self, threads, task_queue=None, result_queue=None):
        self.threads = []
        for _ in range(threads):
            thread = Thread(target=self.__run)
            thread.setDaemon(True)
            self.threads.append(thread)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def __run(self):
        if self.task_queue is None:
            for result in self._run(None):
                self.result_queue.put(result)
        elif self.result_queue is None:
            while True:
                task = self.task_queue.get()
                self._run(task)
                self.task_queue.task_done()
        else:
            while True:
                task = self.task_queue.get()
                result = self._run(task)
                self.result_queue.put(result)
                self.task_queue.task_done()

    def _run(self, task):
        raise NotImplementedError

    def start(self):
        for thread in self.threads:
            thread.start()

    def join(self):
        for thread in self.threads:
            thread.join()

    def _get(self):
        return self.task_queue.get()

    def _put(self, *args):
        self.result_queue.put(*args)


class Task(object):
    def __init__(self, steps, queue_sizes):
        self.steps = steps
        self.queues = [Queue(maxsize=size) for size in queue_sizes]
        self._chain(self.queues)

    def _chain(self, queues):
        """使用队列连接每个阶段的任务
        将队列作为前一个阶段的结果队列，作为后一个阶段的任务队列
        """
        self.steps[0].result_queue = queues[0]
        self.steps[-1].task_queue = queues[-1]
        for i, step in enumerate(self.steps[1:-1], start=1):
            step.task_queue = queues[i - 1]
            step.result_queue = queues[i]

    def start(self):
        """执行任务
        """
        for step in self.steps:
            step.start()

    def join(self):
        """阻塞直到任务的所有步骤执行完毕
        """
        self.steps[0].join()
        for q in self.queues:
            q.join()
