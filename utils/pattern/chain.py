"""
https://github.com/faif/python-patterns/blob/master/behavioral/chain.py
"""


class Handler:
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, request):
        res = self._handle(request)
        if not res:
            self._successor.handle(request)

    def _handle(self, request):
        raise NotImplementedError('Must provide implementation in subclass.')


def coroutine(func):
    # @functools.wrap(func)
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr

    return start
