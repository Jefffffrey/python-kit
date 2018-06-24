from __future__ import absolute_import

from threading import Lock


class LockedIterator(object):
    def __init__(self, it):
        self.lock = Lock()
        self.it = it

    def __iter__(self):
        return self

    def next(self):
        self.lock.acquire()
        try:
            return self.it.next()
        finally:
            self.lock.release()
